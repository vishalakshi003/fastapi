from src.core.database import Base
from sqlalchemy import JSON, Column,String,Integer,DateTime,Boolean,UniqueConstraint
from sqlalchemy.sql import func#it will use to indicate current time 
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from .language import language_users
class CustomUser(Base):
    __tablename__="customuser"
    id=Column(Integer,primary_key=True)
    email=Column(String,unique=True,nullable=False)
    mobile_number=Column(String(32),nullable=False,unique=True)
    password=Column(String,nullable=True) 
    id_proof = Column(ARRAY(JSON), default=list, nullable=False)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    modified_by=Column(String,nullable=True)
    is_active=Column(Boolean,default=True)
    __table_args__=(UniqueConstraint("email","mobile_number",name="unique_users")),
    profile=relationship("UserPersonalProfile",back_populates="users", uselist=False)
    language=relationship("Language",secondary=language_users,back_populates="users")
