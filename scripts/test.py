import asyncio

from sqlalchemy import select

from api_service.database import db as database
from ragit_db.models import Context, File, ContextFile


async def main():
    async with database.session() as session:
        file_query = (
            select(ContextFile, File).join(ContextFile).where(ContextFile.context_id == "86434768-d6f4-4299-b558-4fd33dc14286")
        )
        files = (await session.execute(file_query)).scalars().all()
        print(files)
        for file in files:
            print(file)


asyncio.run(main())
