from src.core.database import async_get_db

async def get_context():
    db_gen=async_get_db()
    db=await db_gen.__anext__()
    try:
        yield {"db": db}
    finally:
        await db_gen.aclose() # it will for close session, in graphql we will override session
