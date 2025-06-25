import strawberry
from strawberry.federation import type as federation_type
from typing import List
@strawberry.input
class Create_Asset:
    name:str
# @strawberry.type
# class GetAsset:
#     id:int
#     name:str



@federation_type(keys=["id"])
class User:
    id: strawberry.ID

    @staticmethod
    def resolve_reference(id: strawberry.ID) -> "User":
        return User(id=id)


@strawberry.type
class GetAsset:
    id: int
    name: str

@strawberry.input
class Create_allocated:
    asset_id:int
    user_id:int
# @strawberry.type
# class GetAssetAllocated:
#     id:int
#     asset_id:int
#     status:str


@strawberry.type
class GetAssetAllocated:
    id:int
    asset_id:GetAsset
    user_id:User
    status:str