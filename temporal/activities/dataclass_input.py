from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

JSON = Dict[str, Any]

@dataclass
class CreateUserInput:
    firstname: str
    lastname: str
    email: str
    mobileNumber: str
    password: str
    password1: str
    middlename: Optional[str] = None
    profilephoto: Optional[JSON] = None
    hobbies: Optional[JSON] = None
    addressInfo: Optional[JSON] = None
    idProof: Optional[JSON] = None
    language: Optional[List[str]] = None
    roles: List[str] = field(default_factory=lambda: ["consumer"])
@dataclass
class UserProfileInput:
    user_id: int
    firstname: str
    lastname: str
    profilephoto: Optional[JSON] = None
    hobbies: Optional[JSON] = None
    addressinfo: Optional[JSON] = None
@dataclass
class RoleMappingInput:
    userId: int
    rolename: List[str]

