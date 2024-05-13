from datetime import datetime
from typing import List

from fastapi import HTTPException, Request
from ragit_db.models import Context
from sqlalchemy import select

from ....clients import qdrant
from ....clients.llm import invoke_groq, invoke_openai
from ....database import db
from ....utils import create_text_embeddings
from .types import ChatRequest, ChatResponse
from .utils import (
    create_chat_history,
    create_playground,
    get_chat_history_by_id,
    get_playground_by_id,
)

sys_prompt = """You are a helpful assistant. Your role is to play a support chat bot to help users with their queries.

You are provided this context. Use this context to give your answers.

--- Context Start ---

{context}

--- Context End ---


"""


sys_prompt_2 = """You are a helpful assistant. Your role is to play a support chat bot to help users with their queries.

Answer the question based only on the following context:
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


async def chat(request: Request, playground_id: str, data: ChatRequest) -> ChatResponse:

    async with db.session() as session:

        context_query = select(Context).where(Context.id == data.context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()

        if not context:
            raise HTTPException(status_code=404, detail="Context not found")

        playground = await get_playground_by_id(playground_id)

        if playground is None:
            pg_id = await create_playground(
                playground_id,
                str(datetime.utcnow()),
                "",
                context.project_id,
                context.id,
                context.owner_id,
            )
            playground = await get_playground_by_id(pg_id)

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
            {
                "role": "user",
                "content": sys_prompt_2.format(
                    context=format_context(docs), query=data.query
                ),
            }
        )
        response = None
        model_provider, model_name = data.model.split(":")
        if model_provider == "groq":
            response = await invoke_groq(
                messages, model_name=model_name, model_params=data.model_params
            )
        elif model_provider == "openai":
            response = await invoke_openai(
                messages, model_name=model_name, model_params=data.model_params
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid model provider")

        ch_id = await create_chat_history(
            playground.id,
            request.state.user_id,
            sys_prompt,
            data.query,
            response,
            "llm",
            {},
            docs,
        )
        chat_history = await get_chat_history_by_id(ch_id)
        return ChatResponse(
            id=chat_history.id,
            playground_id=playground.id,
            user_id=chat_history.user_id,
            system_prompt=chat_history.system_prompt,
            user_prompt=chat_history.user_prompt,
            model_response=chat_history.model_response,
            model=chat_history.model,
            model_params=chat_history.model_params,
            documents=chat_history.documents,
            created_at=str(chat_history.created_at),
        )
