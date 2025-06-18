from pydantic import BaseModel, EmailStr
from typing import Optional,List,Dict,Any
class UserBase(BaseModel):
    firstname:str
    middlename:Optional[str]=None
    lastname:str
    email:EmailStr
    mobile_number:str
    id_proof: Optional[List[Dict[str, Any]]]=None
    profilephoto: Optional[Dict[str, Any]] = None
    hobbies: Optional[List[str]] = []
    address_info:Optional[Dict[str, Any]]=None
    language:Optional[List[str]]=None

class CreateUser(UserBase):
    password:str
    password1:str
    # created_by:int
    # modified_by:int
    roles:Optional[List[str] ]=None

class UserResponse(UserBase):
    id:int




class RoleBase(BaseModel):
    name:str
    desc:Optional[str]=None
class CreateRole(RoleBase):
    pass
class RoleResponse(RoleBase):
    id:int


class LoginRequest(BaseModel):
    mobilenumber:str
    password:str

class CreateLanguage(BaseModel):
    name:str