from src.core.database import Base
from sqlalchemy import Column,Integer,ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class RoleMapping(Base):
    __tablename__="rolemapping"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("customuser.id"))
    role_id=Column(Integer,ForeignKey("rolemaster.id"))
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='unique_user_role'),
    )

    users=relationship("CustomUser")
    roles=relationship("RoleMaster")