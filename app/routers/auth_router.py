from app.services.auth_services import verify_password, hash_password
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schemas import User, UserLogin
from app.database import get_db, Session
from app.models.user_models import UserDB
from datetime import datetime, timezone, timedelta
from jose import jwt
from sqlalchemy import or_
from app.core.config import SECRET_KEY, ALGORITHM



router = APIRouter(prefix="/users")

@router.post("/auth/register")
async def register_user(user: User, db: Session = Depends(get_db)):

    duplicated_user = db.query(UserDB).filter(or_(UserDB.username == user.username,
                                       UserDB.email == user.email)).first()
    
    if duplicated_user:
        raise HTTPException(status_code=401, detail="Invalid username or email")
    
    password = hash_password(user.password)

    new_user = UserDB(username=user.username,
    email=user.email,
    password=password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message" : "User has been registered",
            "username" : user.username}



@router.post("/auth/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):

    
    user_db = db.query(UserDB).filter(or_(UserDB.username == user.identifier, UserDB.email == user.identifier)).first()

    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid user")

    if not verify_password(user.password,user_db.password):
        raise HTTPException(status_code=401,detail="Not authorized")
    
    token = jwt.encode({"user_id" : user_db.id, "exp" : datetime.now(timezone.utc) + timedelta(days=3)}, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token" : token,
            "token_type" : "bearer"}


