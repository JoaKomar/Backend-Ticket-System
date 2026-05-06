from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from app.database import get_db, Session
from jose import jwt, JWTError
from app.core.config import ALGORITHM, SECRET_KEY
from app.models.user_models import UserDB
import bcrypt

oauth2_schema = OAuth2PasswordBearer(tokenUrl="users/auth/login")

#Creation of the token flow to hold session.
def current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=400, detail="Invalid user")
        return user

    except JWTError:
        raise HTTPException(status_code=401,detail="Not authorized")



#Hashing of password. Then we'll save on the database
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

#To verify password if it's same that the saved on the database
def verify_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode(), hashed.encode())


