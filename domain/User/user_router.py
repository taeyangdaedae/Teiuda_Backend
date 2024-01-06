from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from typing_extensions import Annotated

from database import get_db
from domain.User import user_crud, user_schema
from domain.user.user_crud import pwd_context

router = APIRouter(
    prefix="/api/user",
)


@router.post("/signup", status_code=status.HTTP_204_NO_CONTENT)
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
    
    hashed_password = pwd_context.hash(form_data.password)
    
    if not pwd_context.verify(form_data.password, user_dict.password):
        raise HTTPException(status_code=401, detail="password not correct",
                            headers={"WWW-Authenticate": "Bearer"},)

    return {"access_token": access_token, "token_type": "bearer", "userid":user_dict.username}