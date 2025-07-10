from fastapi import HTTPException
import strawberry
from strawberry.types import Info
from src.api.graphql.types import Create_Asset, GetAsset,User,GetAssetAllocated
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.asset import AssetAllocated,Assetmaster
from typing import Optional
from sqlalchemy import select
from typing import List
from shared.core.errors.http_error import HttpError
@strawberry.type
class Query:
    @strawberry.field
    async def get_asset(self,info:Info,id:Optional[int]=None)->List[GetAsset]:
        db:AsyncSession=info.context["db"]
        user=info.context["user"]
        print(user)
        if not user:
            raise HttpError.unauthorized()
        if id:
            results=await db.execute(select(Assetmaster).where(Assetmaster.id==id))
        else:
            results=await db.execute(select(Assetmaster))
        data=results.scalars().all()
        return data
    @strawberry.field
    async def get_asset_allocation(self, info: Info, id: Optional[int] = None) -> List[GetAssetAllocated]:
        db: AsyncSession = info.context["db"]
        
        if id:
            results = await db.execute(select(AssetAllocated).where(AssetAllocated.id == id))
        else:
            results = await db.execute(select(AssetAllocated))
        
        data = results.scalars().all()
        response = []

        for asset in data:
            asset_master_result = await db.execute(select(Assetmaster).where(Assetmaster.id == asset.asset_id))
            asset_master = asset_master_result.scalar_one_or_none()

            if asset_master:
                response.append(GetAssetAllocated(
                    id=asset.id,
                    status=asset.allocated_status,
                    user_id=User(id=str(asset.user_id)),
                    asset_id=GetAsset(
                        id=asset_master.id,
                        name=asset_master.name
                    )
                ))

        return response


