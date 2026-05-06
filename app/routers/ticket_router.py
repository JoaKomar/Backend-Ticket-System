from fastapi import APIRouter, Depends,HTTPException
from app.models.ticket_models import TicketDB
from app.models.user_models import UserDB
from app.database import get_db, Session
from datetime import datetime, timezone
from app.models.comment_models import CommentDB
from app.services.auth_services import current_user
from app.schemas.ticket_schemas import TicketStatus
from app.schemas.comment_schema import Comment
from app.services.ticket_services import search_admin_ticket, can_modify
from app.schemas.ticket_schemas import  TicketUser




router = APIRouter(prefix="/tickets")



#Endpoint to create tickets

@router.post("/")
async def create_ticket(ticket: TicketUser,
                        user: UserDB = Depends(current_user),
                        db: Session = Depends(get_db)):
    
    admin_db = search_admin_ticket(db)

    if not admin_db:
        raise HTTPException(status_code=503, detail="No hay staff para atender el ticket, intente mas tarde")
    

    new_ticket = TicketDB(title=ticket.title,
                          description=ticket.description,
                          updated_at=datetime.now(timezone.utc),
                          owner_id=user.id,
                          assigned_admin_id=admin_db.id
                            )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {"message" : "created ticket"}



#To get tickets

@router.get("/")
async def view_ticket(id: int | None = None,
                      offset: int = 0,
                      limit: int = 10,
                      status: TicketStatus | None = None,
                      user: UserDB = Depends(current_user),
                      db: Session = Depends(get_db)):

    ticket_db = db.query(TicketDB)

    if user.role != "admin":
        ticket_db = ticket_db.filter(TicketDB.owner_id == user.id, TicketDB.is_deleted == False)

    if id:
       ticket_db = ticket_db.filter(TicketDB.id == id)
    
    if status:
        ticket_db = ticket_db.filter(TicketDB.status == status.value)

    ticket_db = ticket_db.order_by(TicketDB.id).offset(offset).limit(limit)

    return ticket_db.all()



@router.post("/comments/{id}")
async def create_comment(id:int,
                         comment: Comment,
                         user: UserDB = Depends(current_user),
                         db: Session = Depends(get_db)):
                         
    ticket = db.query(TicketDB).filter(TicketDB.id == id,TicketDB.owner_id == user.id).first()  

    if not ticket:
        raise HTTPException(status_code=400, detail="Invalid ID")

    new_comment = CommentDB(content=comment.content,
                            ticket_id=ticket.id,
                            owner_id=user.id,
                            admin_id=ticket.assigned_admin_id
                            )
    
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)


    return {"message" : "sent comment",
            "data" : new_comment}


@router.post("/comments/response/{ticket_id}")
async def comment_response(ticket_id: int,comment: Comment, user: UserDB = Depends(current_user), db: Session = Depends(get_db)):

    if user.role != "admin":
        raise HTTPException(status_code=400, detail="bad request")
    
    ticket_db = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()

    if ticket_db:
        comment_response = CommentDB(content=comment.content,
                            ticket_id=ticket_db.id,
                            owner_id=ticket_db.owner_id,
                            admin_id=ticket_db.assigned_admin_id)
    

        db.add(comment_response)
        db.commit()
        db.refresh(comment_response)

        return {"message" : "sent comment",
            "at" : datetime.now(timezone.utc)}
    
    raise HTTPException(status_code=400, detail="Bad request")




@router.get("/comments")
async def view_comments(user: UserDB = Depends(current_user),db: Session = Depends(get_db)):

    comments = db.query(CommentDB)

    if user.role != "admin":
        comments = comments.filter(CommentDB.owner_id == user.id)
    

    return comments.all()


#queda agregar la update del ticket
@router.put("/{id}")
async def update_ticket(id: int, ticket: TicketUser, user: UserDB = Depends(current_user), db: Session = Depends(get_db)):


        ticket_db = db.query(TicketDB).filter(TicketDB.id == id).first()

        if not can_modify(ticket_db, user):
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        ticket_db.title = ticket.title
        ticket_db.description = ticket.description
        ticket_db.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(ticket_db)

        return {"message" : "Updated ticket"}


    

@router.delete("/{id}")
async def delete_ticket(id: int, user: UserDB = Depends(current_user), db: Session = Depends(get_db)):

    ticket_db = db.query(TicketDB).filter(TicketDB.id == id).first()

    if not can_modify(ticket_db,user):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    ticket_db.is_deleted = True
    db.commit()
    db.refresh(ticket_db)

    return {"message" : "Deleted ticket"}