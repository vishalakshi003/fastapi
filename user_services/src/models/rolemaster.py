from sqlalchemy import Column,String,Boolean,Integer,DateTime
from src.core.database import Base
from sqlalchemy.sql import func



class RoleMaster(Base):
    __tablename__="rolemaster"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False,unique=True)
    desc=Column(String,nullable=True)
    created_at=Column(DateTime,server_default=func.now(),nullable=False)
    created_by=Column(String,nullable=False)
    modified_at=Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)
    modified_by=Column(String,nullable=True) 
    is_active=Column(Boolean,default=True)   

