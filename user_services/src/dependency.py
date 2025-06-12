from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException,status
from typing_extensions import Annotated
from src.core.database import async_get_db
from src.utils import fetch_current_user

SessionDeps=Annotated[AsyncSession,Depends(async_get_db)]


##current user
CurrentUserDeps=Annotated[dict,Depends(fetch_current_user)]
