from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.api.graphql.schemas import schema
from src.core.config import config
from src.dependency import get_context
from temporalio.client import Client

from shared.middleware.graphql_status import ForceGraphQLHTTPStatusMiddleware

app=FastAPI()
app.add_middleware(ForceGraphQLHTTPStatusMiddleware)
users=GraphQLRouter(schema,context_getter=get_context)
app.include_router(users,prefix='/graphql')

@app.on_event("startup")
async def startup_event():
    app.temporal_client = await Client.connect(config.TEMPORAL_ADDRESS)
    # app.temporal_client = await Client.connect("localhost:7233")

