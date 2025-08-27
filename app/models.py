from sqlalchemy import Column, String, DateTime, func
from .database import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)
    country = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_seen  = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)