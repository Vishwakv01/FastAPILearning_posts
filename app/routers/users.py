from fastapi import Response, HTTPException, status, Depends, APIRouter
from app import schema, utils
from app.database import get_db
from app import models
from sqlalchemy.orm import session

router = APIRouter(
    tags=['users']
)

@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=schema.ResponseCreatuser)
def creat_user(user: schema.CreateUser, db: session = Depends(get_db)):

    # password hassing...
    hash_password = utils.hash(user.password)
    user.password = hash_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/user/{id}', response_model=schema.ResponseCreatuser)
def get_user(id: int, db: session= Depends(get_db)):
    get_user = db.query(models.Users).filter(models.Users.id == id).first()

    if get_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User Id {id} not foung ")
    return get_user