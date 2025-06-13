from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing_extensions import Annotated
from src.core.database import async_get_db
from src.utils import fetch_current_user,oauth2_scheme
SessionDeps=Annotated[AsyncSession,Depends(async_get_db)]


##current user
CurrentUserDeps=Annotated[dict,Depends(fetch_current_user)]

##oauth
OuthUserDeps=Annotated[dict,Depends(oauth2_scheme)]
