import strawberry

@strawberry.input
class Create_Asset:
    name:str
@strawberry.type
class GetAsset:
    id:int
    name:str
