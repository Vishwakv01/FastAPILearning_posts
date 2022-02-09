from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schema, database, utils, oauth2

router = APIRouter(tags=['authentication'])


@router.post('/login', response_model=schema.Token)
def login(user_cred: OAuth2PasswordRequestForm= Depends(), db: Session= Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_cred.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found in our inverntry")

    if not utils.verify(user_cred.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Enter password is mismatching..')
    

    access_token = oauth2.create_token(data= {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

