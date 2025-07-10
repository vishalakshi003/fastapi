from src.core.database import async_get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from typing_extensions import Annotated
from src.core.database import async_get_db
# from src.utils import fetch_current_user, jwt_decode_payload,oauth2_scheme
from shared.utils.jwt import jwt_decode_payload
# async def get_context():
#     db_gen=async_get_db()
#     db=await db_gen.__anext__()
#     try:
#         yield {"db": db}
#     finally:
#         await db_gen.aclose() # it will for close session, in graphql we will override session



async def get_context(request: Request, db: AsyncSession = Depends(async_get_db)):
    user = None
    auth_header = request.headers.get("authorization")
    print("Authorization header:", auth_header)
    print('888888888888888888888888')
    if auth_header:
        token = auth_header.split(" ")[1]
        try:
            decoded = jwt_decode_payload(token)
            print("decoded full payload:", decoded)
            print('decode------------------',decoded)
            user = decoded.get("email")
            print('user----------------',user)
        except Exception as e:
            user = None
    print('usersssss',user)
    return {
        "db": db,
        "user": user,
        # "temporal_client": request.app.temporal_client,
    }
