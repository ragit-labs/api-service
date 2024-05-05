from typing import List

from fastapi import APIRouter, HTTPException, Request
from ragit_db.models import Context
from sqlalchemy import select

from api_service.clients import qdrant
from api_service.clients.llm import LLMMessage, invoke_groq
from api_service.database import db
from api_service.utils import create_text_embeddings

from .types import ChatRequest

router = APIRouter(tags=["chat"])

sys_prompt = """You are provided this context. Use this context to give your answers.

--- Context Start ---

{context}

--- Context End ---


"""


sys_prompt_2 = """Answer the question based only on the following context:
{context}

Question: {query}

Context is a JSON array, each with 2 keys - context_index and context_content.
When using a context for your answer, provide context_index appended to the sentence in this format: [context_index]
Do not mention that you used context. Act like a customer support chat bot.
"""


def format_context(docs: List[str]):
    return "\n\n".join(
        str({"context_index": i, "context_content": doc}) for i, doc in enumerate(docs)
    )


@router.post("/chat")
async def search(request: Request, data: ChatRequest):
    async with db.session() as session:
        context_query = select(Context).where(Context.id == data.context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")

        max_len = context.max_doc_length
        query_embedding = list(
            create_text_embeddings([data.query], max_len, context.embedding_model)
        )[0]
        docs_to_retrieve = context.docs_to_retrieve
        search_results = qdrant.search(
            collection_name=data.context_id,
            query_vector=query_embedding.tolist(),
            limit=docs_to_retrieve,
        )
        docs = []
        for result in search_results:
            if result.payload:
                docs.append(result.payload["document"])

        messages = []
        messages.append(
            LLMMessage(
                role="user",
                content=sys_prompt_2.format(
                    context=format_context(docs), query=data.query
                ),
            )
        )
        response = await invoke_groq(messages)

        return {"response": response, "documents_used": docs}
