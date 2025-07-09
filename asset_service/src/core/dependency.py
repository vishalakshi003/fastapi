from src.core.database import async_get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from typing_extensions import Annotated
from src.core.database import async_get_db
# from src.utils import fetch_current_user, jwt_decode_payload,oauth2_scheme
from shared.jwt_utils import jwt_decode_payload
# async def get_context():
#     db_gen=async_get_db()
#     db=await db_gen.__anext__()
#     try:
#         yield {"db": db}
#     finally:
#         await db_gen.aclose() # it will for close session, in graphql we will override session



async def get_context(request: Request, db: AsyncSession = Depends(async_get_db)):
    user = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            decoded = jwt_decode_payload(token)
            user = decoded.get("sub") or decoded.get("id")
        except Exception as e:
            user = None

    return {
        "db": db,
        "user": user,
        "temporal_client": request.app.temporal_client,
    }
