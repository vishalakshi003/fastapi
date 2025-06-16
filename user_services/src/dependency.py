from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from typing_extensions import Annotated
from src.core.database import async_get_db
from src.utils import fetch_current_user,oauth2_scheme
async def get_context(request:Request):
    db_gen=async_get_db()
    db=await db_gen.__anext__()
    async def shutdown():
        try:
            await db_gen.aclose()
        except Exception as e:
            print("Error closing DB generator:", e)
    return {"db":db,"shutdown":shutdown}

SessionDeps=Annotated[AsyncSession,Depends(async_get_db)]


##current user
CurrentUserDeps=Annotated[dict,Depends(fetch_current_user)]

##oauth
OuthUserDeps=Annotated[dict,Depends(oauth2_scheme)]
