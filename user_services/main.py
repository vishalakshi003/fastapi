from fastapi import FastAPI
from src.routes.users_routes import user_router
from src.routes.role import role_router
app=FastAPI()
app.include_router(user_router,prefix="/users/api",tags=["users"])
app.include_router(role_router,prefix="/users/api",tags=["users"])
