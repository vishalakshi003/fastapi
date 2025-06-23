from sqlalchemy import create_engine
from .config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager
Base=declarative_base()
sync_engine=create_engine("postgresql://postgres:vishali@localhost:5432/fastapi_demo")

Sync_Session=sessionmaker(autocommit=False,autoflush=False,bind=sync_engine)

def get_session():
    session=Sync_Session()
    try:
        yield session
    finally:
        session.close()

async_engine=create_async_engine(Config.DATABASE_URL)

async def async_get_db():
    AsyncSessionMaker=sessionmaker(bind=async_engine,class_=AsyncSession,expire_on_commit=False)

    async with AsyncSessionMaker() as session:
        yield session
