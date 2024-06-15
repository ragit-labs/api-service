from fastapi import Request, HTTPException
from typing import List
from ....database import db
from ragit_db.models import Embedding1536, Discord
from sqlalchemy import select
from ....clients.llm import generate_openai_embeddings
from .types import DiscordChatResponse, DiscordChatRequest
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")


model = ChatOpenAI(model="gpt-3.5-turbo", api_key="sk-proj-FMnd5Ng5LlgMjqQwi2kqT3BlbkFJOR5D7bmsro9YrjqFdOwu")


system_prompt__1 = """You're a support agent that is talking to a customer. Use only the chat history and the following information
{context}
to answer in a helpful manner to the question. If you don't know the answer - say that you don't know.
Keep your replies short, compassionate and informative.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt__1,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{query}"),
    ]
)

runnable = prompt | model


runnable_with_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="query",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(id="channel_id", annotation=str, name="Thread ID", description="The ID of the thread in which the conversation is taking place.", default="", is_shared=True),
    ]
)


sys_prompt = """You are a helpful assistant. Your role is to play a support chat bot to help users with their queries.
Do not mention that you used context. Act like a customer support chat bot. Also provide links to the relevant support pages if necessary.
After every chat, ask the user if they have any other queries. If you don't have context of the query, simply respond that you don't know.
"""

sys_prompt_1 = """You are a helpful assistant. You will be rewarded for answering user queries using a context provided to you.
Do not mention that you used context. Also provide links to the relevant support pages if necessary.
If no context is provided, do not answer the question or you will be penalized.
After every chat, ask the user if they have any other queries.
"""


prompt = """You are a helpful assistant. Your role is to play a support chat bot to help users with their queries.
Do not mention that you used context. Act like a customer support chat bot. Also provide links to the relevant support pages if necessary.
After every chat, ask the user if they have any other queries.

Answer the question based only on the following context. Keep your answer very concise. Do not return markdown. Give supporting urls.
If the answer is long, break it into multiple answers.


{context}

----

Question: {query}

Return a JSON object with the key 'answers' and the value as the answer array. Do not repeat any answer. It's not required to use all context, only use the relevant parts.
"""


prompt_2 = """You are a helpful assistant. Your role is to play a support chat bot to help users with their queries.

Answer the question based only on the following context:
{context}

Question: {query}


Do not mention that you used context. Act like a customer support chat bot. Also provide links to the relevant support pages if necessary.
After every chat, ask the user if they have any other queries.
"""


prompt_3 = """You are an AI customer support agent name "Morty". You are a part of the RentoMojo team. You will be provided with two pieces of information:

<context>
{context}
</context>

This is background information and context that may be useful for answering customer queries.

<query>
{query}
</query>

This is a question or request from a customer that you need to respond to.

Carefully read through the context provided. Think about how you can use that information to address the customer's query. 

<scratchpad>
Write down your initial thoughts and ideas here for how to respond to the customer, based on the context provided. What parts of the context seem most relevant? How can you succinctly but thoroughly address the key points in the customer's query? Are there any gaps where you need more information from the customer to better assist them?
</scratchpad>

Do not mention that you used context. Provide your response to the customer directly. Aim to directly address their query as best you can using the context available. Be thorough but concise. Provide any links if required.

If there are aspects of the query you cannot fully address with the given context, politely ask the customer for any additional information or clarification you need. Something like "To better assist you with [X], could you please provide some more details on [Y]?" Focus your response on addressing the customer's specific needs.

Do not say anything that is not directly relevant to answering the query based on the provided context. If the query cannot be answered at all based on the context, politely inform the customer of this, and ask them if you should connect them to a Human Representative from the team.

Remember, your goal is to be a helpful, friendly, and efficient customer support agent. Always respond professionally and on-topic.
"""


prompt_4 = """You are an AI customer support agent. You will be provided with two pieces of information:

<context>
{context}
</context>

This is background information and context that may be useful for answering customer queries.

<query>
{query}
</query>

This is a question or request from a customer that you need to respond to.

Carefully read through the context provided. Think about how you can use that information to address the customer's query. 

Do not mention that you used context. Provide your response to the customer directly. Aim to directly address their query as best you can using the context available. Be thorough but concise. Provide any links if required.

If there are aspects of the query you cannot fully address with the given context, politely ask the customer for any additional information or clarification you need. Something like "To better assist you with [X], could you please provide some more details on [Y]?" Focus your response on addressing the customer's specific needs.

Do not say anything that is not directly relevant to answering the query based on the provided context. If the query cannot be answered at all based on the context, politely inform the customer of this, and ask them if you should connect them to a Human Representative from the team.

Remember, your goal is to be a helpful, friendly, and efficient customer support agent. Always respond professionally and on-topic. It no context is provided, don't answer the question.
"""


prompt_5 = """You are a helpful assistant. You will be rewarded for answering user queries using a context provided to you.
Do not mention that you used context. Also provide links to the relevant support pages if necessary.
If no context is provided, do not answer the question or you will be penalized.
After every chat, ask the user if they have any other queries.

This is background information and context that may be useful for answering customer queries.

<context>
{context}
</context>

This is a question or request from a customer that you need to respond to.

<query>
{query}
</query>

Remember, your goal is to be a helpful, friendly, and efficient customer support agent. Always respond professionally and on-topic. It no context is provided, don't answer the question.
"""


def format_context(docs: List[str]):
    return "\n\n".join(doc for doc in docs)


async def discord_chat(
    request: Request, data: DiscordChatRequest
) -> DiscordChatResponse:
    query_embedding = (await generate_openai_embeddings([data.message]))[0].embedding
    async with db.session() as session:
        discord_query = select(Discord).where(Discord.guild_id == str(data.guild_id))
        discord_result = (await session.execute(discord_query)).scalar_one_or_none()
        if discord_result is None:
            raise HTTPException(
                status_code=404, detail=f"Discord with id {data.guild_id} not found."
            )
        _project_id = discord_result.project_id
        docs_query = select(Embedding1536).where(Embedding1536.project_id == _project_id).order_by(Embedding1536.vector.cosine_distance(query_embedding)).limit(4)
        docs_result = (await session.execute(docs_query)).scalars().all()
        docs = [doc.document for doc in docs_result]
        res: AIMessage = runnable_with_history.invoke(
            {"context": format_context(docs), "query": data.message},
            config={"configurable": {"channel_id": str(data.channel_id)}},
        )
        history = get_session_history(str(data.channel_id))
        msgs = history.messages
        for msg in msgs:
            print(msg.content)
    return DiscordChatResponse(response=res.content)
