from src.core.database import Base
from sqlalchemy import Column,Integer,ForeignKey
from sqlalchemy.orm import relationship

class RoleMapping(Base):
    __tablename__="rolemapping"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("customuser.id"))
    role_id=Column(Integer,ForeignKey("rolemaster.id"))

    users=relationship("CustomUser",back_populates="user")
    roles=relationship("RoleMaster",back_populates="role")