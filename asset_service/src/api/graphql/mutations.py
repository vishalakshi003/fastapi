import strawberry
from strawberry.types import Info
from src.api.graphql.types import Create_Asset, GetAsset
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.asset import AssetAllocated,Assetmaster
from src.schema.asset_schema import *
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_asset(self,data:Create_Asset,info:Info)->GetAsset:
        db:AsyncSession=info.context["db"]
        validated =CreateAsset(**data.__dict__)
        asset=Assetmaster(name=validated.name, created_by=str(1))
        db.add(asset)
        await db.commit()
        await db.refresh(asset)
        return asset        
    # @strawberry.mutation
    # async def assetallocated_to_user():
    #     pass