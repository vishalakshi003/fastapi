from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from typing_extensions import Annotated
from src.core.database import async_get_db
from src.utils import fetch_current_user, jwt_decode_payload,oauth2_scheme
# async def get_context(request:Request):
#     db_gen=async_get_db()
#     db=await db_gen.__anext__()
#     try:
#         yield {"db": db}
#     finally:
#         await db_gen.aclose() 

SessionDeps=Annotated[AsyncSession,Depends(async_get_db)]


##current user
CurrentUserDeps=Annotated[dict,Depends(fetch_current_user)]

##oauth
OuthUserDeps=Annotated[dict,Depends(oauth2_scheme)]

# async def get_context(db: AsyncSession = Depends(async_get_db)):
#     return {"db": db}

# async def get_context(db: AsyncSession = Depends(async_get_db)):
#     return {"db": db}


async def get_context(request: Request, db: AsyncSession = Depends(async_get_db)):
    user = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        user = jwt_decode_payload(token)
        user = user["id"]

    return {
        "db": db,
        "user": user,
        # "temporal_client": request.app.temporal_client,
    }
