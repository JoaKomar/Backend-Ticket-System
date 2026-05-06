from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

#Models of Ticket structure
class TicketDB(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    assigned_admin_id = Column(Integer, nullable=False)
    
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="tickets")
    
    comments = relationship("CommentDB", back_populates="ticket")
