import strawberry
from strawberry.types import Info
from src.api.graphql.types import Create_Asset, GetAsset,Create_allocated,GetAssetAllocated, User
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.asset import AssetAllocated,Assetmaster
from src.schema.asset_schema import *
from shared.core.errors.http_error import HttpError
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_asset(self,data:Create_Asset,info:Info)->GetAsset:
        db:AsyncSession=info.context["db"]
        user=info.context["user"]
        if not user:
            raise HttpError.unauthorized()
        validated =CreateAsset(**data.__dict__)
        asset=Assetmaster(name=validated.name, created_by=str(1))
        db.add(asset)
        await db.commit()
        await db.refresh(asset)
        return asset        
    @strawberry.mutation
    async def create_assetallocated(self,data:Create_allocated,info:Info)->GetAssetAllocated:
        db:AsyncSession=info.context["db"]
        allocated=AssetAllocated(asset_id=data.asset_id,user_id=data.user_id,created_by=str(data.user_id))
        db.add(allocated)
        await db.commit()
        await db.refresh(allocated)
        asset = await db.get(Assetmaster, data.asset_id)

        return GetAssetAllocated(
            id=allocated.id,
            status=allocated.allocated_status,
            asset_id=GetAsset(id=asset.id, name=asset.name),
            user_id=User(id=str(allocated.user_id))
        )
