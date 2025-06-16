import strawberry
from .types import Get_role
from typing import Optional
from ...dependency import SessionDeps
from sqlalchemy import select
from ...models.rolemaster import RoleMaster
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession
@strawberry.type
class Query:
    @strawberry.field
    async def get_roles(self,info:Info,id:Optional[int]=None)-> Get_role:
        db: AsyncSession = info.context["db"]
        if id:
            results=await db.execute(select(RoleMaster).where(RoleMaster.id==id))
        else:
            results=await db .execute(select(RoleMaster))
        roles=results.scalars().all()
        return roles
