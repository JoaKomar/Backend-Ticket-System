from app.database import get_db, Session
from fastapi import Depends, HTTPException
from app.models.user_models import UserDB
from app.schemas.user_schemas import User
from app.models.ticket_models import TicketDB
from sqlalchemy import func



#To find a specify admin

def search_admin_ticket(db: Session = Depends(get_db)):

    selected_admin = (db.query(UserDB)
    .outerjoin(TicketDB, UserDB.id == TicketDB.assigned_admin_id)
    .filter(UserDB.role == "admin")
    .group_by(UserDB.id)
    .order_by(func.count(TicketDB.id).asc())
    .first()) 
    
    return selected_admin
    


#To find a specify user

def search_user(user: User,db: Session = Depends(get_db)):
    user_db = db.query(UserDB).filter(UserDB.username == user.username).first()

    if user_db:
        return user_db
    raise HTTPException(status_code=404, detail="Not Found")


#we'll use it for a put or delete endpoint.

def can_modify(ticket: TicketDB, user: UserDB):
    if user.role == "admin":
        return True
    return ticket.owner_id == user.id
    