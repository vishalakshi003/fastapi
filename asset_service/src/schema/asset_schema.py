from pydantic import BaseModel


class AssetBase(BaseModel):
    name:str
class CreateAsset(AssetBase):
    pass
class AssetResponse(AssetBase):
    id:int

class CreateAllocatedUser(BaseModel):
    asset_id:int
    user:int
class AllocatedResponse(BaseModel):
    id:int
    asset:AssetResponse
    user:int

