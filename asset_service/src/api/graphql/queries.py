import strawberry
from strawberry.types import Info
from src.api.graphql.types import CreateAsset, GetAsset
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.asset import AssetAllocated,Assetmaster
from typing import Optional
from sqlalchemy import select
from typing import List
@strawberry.type
class Query:
    @strawberry.field
    async def get_asset(self,info:Info,id:Optional[int]=None)->List[GetAsset]:
        db:AsyncSession=info.context["db"]
        if id:
            results=await db.execute(select(Assetmaster).where(Assetmaster.id==id))
        else:
            results=await db.execute(select(Assetmaster))
        data=results.scalars().all()
        return data

