import strawberry
from typing import List,Optional
from pydantic import BaseModel
from typing import Any,Dict
import strawberry
from strawberry.scalars import JSON
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
@strawberry.input
class Create_user:
    firstname:str
    lastname:str
    email:str
    mobile_number:str
    password:str
    password1:str
    profilephoto:JSON
    hobbies: JSON
    address_info:JSON
    language:Optional[List[str]] = None
    roles: Optional[List[str]] = strawberry.field(default_factory=lambda: ["consumer"])

@strawberry.type
class User_details:
    user_id:int
    firstname:str
    lastname:str
    email:str
    mobile_number:str
    id_proof:JSON
    profilephoto:JSON
    hobbies: JSON
    address_info:JSON
    language:Optional[List[GetLang]]
    roles:Optional[str]

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
    status:str
    message:str

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

