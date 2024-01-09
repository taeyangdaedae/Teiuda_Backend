from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status
from typing_extensions import Annotated

from database import get_db
from domain.User import user_crud, user_schema
from domain.User.user_crud import pwd_context



router = APIRouter(
    prefix="/api/user",
)

SECRET_KEY = "d30512f2007bf2cdec338a95cb25988181252f57b6dc5dfe35d559c023928ee8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)
    
    
@router.post("/login", response_model = user_schema.Usertoken)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                    db: Session = Depends(get_db)):
    user_dict = user_crud.get_user(db, form_data.username)
    if not user_dict:
        raise HTTPException(status_code=404, detail="ID not Found")
    
    if not pwd_context.verify(form_data.password, user_dict.password):
        raise HTTPException(status_code=401, detail="password not correct",
                            headers={"WWW-Authenticate": "Bearer"},)
       
    data = {
        "sub" : user_dict.name,
        "exp" : datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "userid": user_dict.name
    }

@router.get("/check/{userid}", status_code=status.HTTP_200_OK)
def double_check_id(userid: str,db: Session = Depends(get_db)):
    result = user_crud.doublecheckid(db, userid)
    if result == True:
        raise HTTPException(status_code=409, detail="id already exist")
    else:
        return{
            "id" : userid
        }
        
        
@router.get("/check/{useremail}", status_code=status.HTTP_200_OK)
def double_check_email(useremail: str,db: Session = Depends(get_db)):
    result = user_crud.doublecheckemail(db, useremail)
    if result == True:
        raise HTTPException(status_code=409, detail="id already exist")
    else:
        return{
            "email" : useremail
        }
        
        