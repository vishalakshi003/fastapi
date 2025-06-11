from sqlalchemy.orm import Mapped,mapped_column,relationship
from src.core.database import Base
from sqlalchemy import ForeignKey

from src.models.customuser import CustomUser
class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("customuser.id"))
    user: Mapped["CustomUser"] = relationship(back_populates="addresses")