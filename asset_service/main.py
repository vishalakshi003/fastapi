from fastapi import FastAPI
from src.api.graphql.schemas import schema
from src.core.dependency import get_context
from strawberry.fastapi import GraphQLRouter
from shared.middleware.graphql_status import ForceGraphQLHTTPStatusMiddleware
from src.core.config import config
from temporalio.client import Client
app=FastAPI()
app.add_middleware(ForceGraphQLHTTPStatusMiddleware)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://localhost:4000"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

asset=GraphQLRouter(schema,context_getter=get_context)
app.include_router(asset,prefix='/graphql')



@app.on_event("startup")
async def startup_event():
    app.temporal_client = await Client.connect(config.TEMPORAL_ADDRESS)
    # app.temporal_client = await Client.connect("localhost:7233")