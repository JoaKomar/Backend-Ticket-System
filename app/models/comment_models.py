from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

#Model of Comment structure
class CommentDB(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(DateTime,default=datetime.now(timezone.utc))

    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    ticket = relationship("TicketDB", back_populates="comments")

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="comments")

    admin_id = Column(Integer, nullable=False)
