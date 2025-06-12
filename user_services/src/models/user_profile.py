from sqlalchemy import ARRAY, JSON, Column, ForeignKey, Integer, String,DateTime,Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class UserPersonalProfile(Base):
    __tablename__ = "user_personal_profile"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("customuser.id"), unique=True, nullable=False)
    firstname = Column(String)
    middlename = Column(String)
    lastname = Column(String)
    profilephoto = Column(JSON, default=dict,nullable=True)
    hobbies = Column(ARRAY(String), default=[])
    address_info = Column(JSON, default=dict, nullable=False) 
    created_at=Column(DateTime,server_default=func.now(),nullable=False)
    created_by=Column(String,nullable=False)
    modified_at=Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)
    modified_by=Column(String,nullable=True) 
    is_active=Column(Boolean,default=True)   

    users=relationship("CustomUser",back_populates="profile")
