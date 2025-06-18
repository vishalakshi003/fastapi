from sqlalchemy import Boolean, Column, DateTime,String,INTEGER,Table,ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
from sqlalchemy.sql import func

language_users=Table(
    'users_language',
    Base.metadata,
    Column('user_id', ForeignKey('customuser.id'), primary_key=True),
    Column('language_id', ForeignKey('language.id'), primary_key=True)
)


class Language(Base):
    __tablename__='language'
    id=Column(INTEGER,primary_key=True)
    name=Column(String,nullable=False)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by=Column(String,nullable=True)
    modified_by=Column(String,nullable=True)
    is_active=Column(Boolean,default=True)

    users=relationship("CustomUser",secondary=language_users,back_populates='language')
