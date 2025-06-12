from pydantic import BaseModel
from typing import Optional,List,Dict,Any
class UserBase(BaseModel):
    firstname:str
    middlename:Optional[str]=None
    lastname:str
    email:str
    mobile_number:str
    id_proof: List[Dict[str, Any]]
    profilephoto: Optional[Dict[str, Any]] = None
    hobbies: Optional[List[str]] = []
    address_info:Optional[Dict[str, Any]]=None

class CreateUser(UserBase):
    password:str
    # created_by:int
    # modified_by:int
    roles: List[str] 

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