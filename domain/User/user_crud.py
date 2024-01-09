from passlib.context import CryptContext
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from datetime import datetime
from domain.User.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    tempuid = uuid.uuid4()
    db_user = User(uid=str(tempuid),
                    id=user_create.userid,
                    name=user_create.username,
                    password=pwd_context.hash(user_create.password1),
                    email=user_create.email,
                    created_at=datetime.now(),
                    updated_at=datetime.now())
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.id == user_create.userid) |
        (User.email == user_create.email)
    ).first()
    

def get_user(db: Session, username: str):
    return db.query(User).filter(User.name == username).first()
    
    
def doublecheckid(db: Session, userid: str):
    result = db.query(User).filter(User.id == userid).first()
    
    if result:
        return True
    else:
        return False


def doublecheckemail(db: Session, useremail: str):
    result = db.query(User).filter(User.email == useremail).first()
    
    if result:
        return True
    else:
        return False

