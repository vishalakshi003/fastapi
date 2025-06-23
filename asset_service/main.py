from fastapi import FastAPI
from src.api.graphql.schemas import schema
from src.core.dependency import get_context
from strawberry.fastapi import GraphQLRouter

app=FastAPI()
asset=GraphQLRouter(schema,context_getter=get_context)
app.include_router(asset,prefix='/graphql')