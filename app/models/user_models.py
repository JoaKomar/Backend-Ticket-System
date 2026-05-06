from sqlalchemy import Column, String, Integer, DateTime, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

#Models of User structure
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    busy = Column(Boolean, default=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    tickets = relationship("TicketDB",back_populates="owner")
    comments = relationship("CommentDB", back_populates="owner")
    