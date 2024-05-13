from datetime import datetime

from fastapi import HTTPException
from ragit_db.models import ChatHistory, Playground
from sqlalchemy import select

from ....database import db


async def create_playground(
    playground_id: str,
    name: str,
    description: str,
    project_id: str,
    context_id: str,
    owner_id: int,
) -> Playground:
    async with db.session() as session:
        get_context_query = select(Playground).where(
            Playground.project_id == project_id, Playground.name == name
        )
        get_context_result = (
            await session.execute(get_context_query)
        ).scalar_one_or_none()
        if get_context_result is not None:
            raise HTTPException(
                status_code=409,
                detail=f"Context by the name {name} already exists in this project.",
            )

        last_playground_query = (
            select(Playground)
            .where(Playground.project_id == project_id)
            .order_by(Playground.id.desc())
            .limit(1)
        )
        last_playground_result = (
            await session.execute(last_playground_query)
        ).scalar_one_or_none()
        readable_id = 1
        if last_playground_result is not None:
            readable_id = last_playground_result.readable_id + 1

        new_playground = Playground(
            id=playground_id,
            name=name,
            description=description,
            readable_id=readable_id,
            project_id=project_id,
            context_id=context_id,
            owner_id=owner_id,
        )
        session.add(new_playground)
        await session.flush()
        await session.refresh(new_playground)
        pg_id = str(new_playground.id)
        await session.commit()
        return pg_id


async def get_playground_by_id(playground_id: str) -> Playground:
    async with db.session() as session:
        get_playground_query = select(Playground).where(Playground.id == playground_id)
        playground = (await session.execute(get_playground_query)).scalar_one_or_none()
        # if not playground:
        #     raise HTTPException(status_code=404, detail="Playground not found")
        return playground


async def create_chat_history(
    playground_id: str,
    user_id: str,
    system_prompt: str,
    user_prompt: str,
    model_response: str,
    model: str,
    model_params: dict,
    documents: list[str],
) -> ChatHistory:
    async with db.session() as session:
        new_chat_history = ChatHistory(
            playground_id=playground_id,
            user_id=user_id,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
            model_response=model_response,
            model_params=model_params,
            documents=documents,
            created_at=datetime.utcnow(),
        )
        session.add(new_chat_history)
        await session.flush()
        await session.refresh(new_chat_history)
        ch_id = str(new_chat_history.id)
        await session.commit()
        return ch_id


async def get_chat_history_by_id(chat_history_id: str) -> ChatHistory:
    async with db.session() as session:
        get_chat_history_query = select(ChatHistory).where(
            ChatHistory.id == chat_history_id
        )
        chat_history = (
            await session.execute(get_chat_history_query)
        ).scalar_one_or_none()
        return chat_history


async def get_chat_history_by_playground_id(playground_id: str) -> list[ChatHistory]:
    async with db.session() as session:
        get_chat_history_query = select(ChatHistory).where(
            ChatHistory.playground_id == playground_id
        )
        chat_history = (await session.execute(get_chat_history_query)).scalars().all()
        return chat_history
