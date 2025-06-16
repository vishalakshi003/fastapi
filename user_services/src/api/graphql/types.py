import strawberry
from typing import List,Optional
from pydantic import BaseModel



@strawberry.input
class Create_user:
    firstname:str
    lastname:str
    email:str
    mobile_number:str
    password:str
    password1:str
    roles: Optional[List[str]] = strawberry.field(default_factory=lambda: ["consumer"])

@strawberry.type
class User_details:
    id:int
    firstname:str
    lastname:str
    email:str
    mobile_number:str
    id_proof:str
    roles:str

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
