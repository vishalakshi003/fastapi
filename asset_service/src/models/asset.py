from sqlalchemy import Column, DateTime,String,Integer,Boolean,ForeignKey
from ..core.database import Base
from sqlalchemy.sql import func

class Assetmaster(Base):
    __tablename__='asset_master'
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    created_at=Column(DateTime,server_default=func.now(),nullable=False)
    created_by=Column(String,nullable=False)
    modified_at=Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)
    modified_by=Column(String,nullable=True) 
    is_active=Column(Boolean,default=True)   

class AssetAllocated(Base):
    __tablename__='allocated_to_users'
    id=Column(Integer,primary_key=True)
    asset_id=Column(Integer,ForeignKey('asset_master.id'),nullable=False)
    user_id=Column(Integer,nullable=False)
    allocated_status=Column(String,default='active',nullable=True)
    created_at=Column(DateTime,server_default=func.now(),nullable=False)
    created_by=Column(String,nullable=False)
    modified_at=Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)
    modified_by=Column(String,nullable=True) 
    is_active=Column(Boolean,default=True)  