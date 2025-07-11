from sqlalchemy import select
import strawberry
from typing import List,Optional
from pydantic import BaseModel
from typing import Any,Dict
import strawberry
from strawberry.scalars import JSON
from strawberry.federation import type as fed_type
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import async_get_db,AsyncSessionMaker
from src.models.customuser import CustomUser
# from shared.core.response import Response
@strawberry.scalar(description="The `JSON` scalar type represents arbitrary JSON values.")
class JSON:
    @staticmethod
    #response
    def serialize(value: Any) -> Any:
        return value

    @staticmethod
    #request
    def parse_value(value: Any) -> Any:
        return value

@strawberry.input
class Create_Lang:
    name:str
@strawberry.type
class GetLang:
    id:int
    name:str
@strawberry.type
class Asset:
    id:int
    name:str
@strawberry.input(name="Createuser")
class Create_user:
    firstname:str
    lastname:str
    middlename: Optional[str] = None 
    email:str
    mobileNumber:str
    password:str
    password1:str
    profilephoto: Optional[JSON] = None  
    hobbies: Optional[JSON] = None      
    addressInfo: Optional[JSON] = None  
    idProof:Optional[JSON]=None
    language:Optional[List[str]] = None
    roles: Optional[List[str]] = strawberry.field(default_factory=lambda: ["consumer"])
    
@strawberry.input
class UserProfileInput:
    user_id: int
    firstname: str
    lastname: str
    profilephoto: Optional[JSON] = None  
    hobbies: Optional[JSON] = None      
    addressinfo: Optional[JSON] = None  
@strawberry.type
class User_details:
    userId:int
    firstname:str
    lastname:str
    email:str
    mobileNumber:str
    idProof:JSON
    profilephoto:JSON
    hobbies: JSON
    addressInfo:JSON
    language:Optional[List[GetLang]]
    roles: List[str]

@strawberry.input
class Create_role:
    name:str
    desc:str
@strawberry.type
class Get_role:
    id:int
    name:str
    desc:str

@strawberry.type
class ResponseMessage:
    status: str
    message: str
    combined_result: Optional[User_details] = None
@strawberry.type
class UserCreateResponse(ResponseMessage):
    userId: str


@strawberry.type
class ErrorResponse:
    status:str
    message: str
    status_code: int

@strawberry.type
class SuccessResponse:
    status:str
    message: str
    status_code: int

@strawberry.input
class LoginReq:
    mobile_no:str
    password:str
@strawberry.type
class TokenRes:
    status:SuccessResponse
    token:str



@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    email: str

    @staticmethod
    async def resolve_reference(id: strawberry.ID, info: strawberry.Info) -> "User":
        async with AsyncSessionMaker() as db:
            # db: AsyncSession = info.context["db"]
            result = await db.execute(
                select(CustomUser).where(CustomUser.id == int(id))
            )
            user = result.scalar_one_or_none()
            if user:
                return User(id=user.id, email=user.email)
            return None
        

@strawberry.type
class RoleMappingType:
    id: int
    roleId: int
    userId: int


@strawberry.input
class RoleMappingInput:
    userId: int
    rolename: List[str]
@strawberry.type
class LangType:
    id: int
    lang_id: int
    user_id: int
@strawberry.input
class LangInput:
    user_id: int
    language: str


@strawberry.type
class CustomUser_details:
    userId:int
    email:str
    mobileNumber:str
    idProof:JSON
    profilephoto:JSON
    hobbies: JSON
    

@strawberry.type
class Userprofile_details:
    id:int
    userId:int
    firstname:str
    lastname:str
    profilephoto:JSON
    hobbies: JSON
    addressInfo:JSON



@strawberry.type
class Response:
    success:bool
    error:Optional[str]=None