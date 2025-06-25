from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.api.graphql.schemas import schema
from src.dependency import get_context
# from src.routes.users_routes import user_router
# from src.routes.role import role_router

app=FastAPI()
users=GraphQLRouter(schema,context_getter=get_context)
app.include_router(users,prefix='/graphql')


# with open("schema.graphql", "w") as f:
#     f.write(schema.as_str())
# app.include_router(user_router,prefix="/users/api",tags=["users"])
# app.include_router(role_router,prefix="/users/api",tags=["users"])
