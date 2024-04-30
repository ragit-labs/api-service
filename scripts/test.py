import asyncio

from sqlalchemy import select

from api_service.database import db as database
from ragit_db.models import Context, File, file_context_association


async def main():
    async with database.session() as session:
        q = select(file_context_association)
        res = await session.execute(q)
        contexts = res.scalars().all()
        for context in contexts:
            print(context)


asyncio.run(main())
