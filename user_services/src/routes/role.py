from fastapi import APIRouter,Depends
from sqlalchemy.future import select
from src.schemas.user_schema import CreateRole
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import async_get_db
from src.models.rolemaster import RoleMaster
from typing import Optional
role_router=APIRouter()

@role_router.post("/role",status_code=201)
async def create_role(data:CreateRole,db:AsyncSession=Depends(async_get_db)):
    new_role=RoleMaster(**data.model_dump())
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role
@role_router.get("/role")
async def get_role(id:Optional[int]=None,db:AsyncSession=Depends(async_get_db)):
    if id:
        results=await db.execute(select(RoleMaster).where(RoleMaster.id==id))
    else:
        results=await db.execute(select(RoleMaster))
    roles = results.scalars().all()
    return roles