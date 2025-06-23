from .config import Config
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
Base=declarative_base()
engine=create_async_engine(Config.DATABASE_URL)

async def async_get_db():
    async_session=sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
    async with async_session() as session:
        yield session
        
