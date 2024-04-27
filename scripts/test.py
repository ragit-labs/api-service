from api_service.database import db as database
import asyncio
from db.models import Context, File, file_context_association
from sqlalchemy import select

async def main():
    async with database.session() as session:
        q = select(file_context_association)
        res = await session.execute(q)
        contexts = res.scalars().all()
        for context in contexts:
            print(context)

asyncio.run(main())