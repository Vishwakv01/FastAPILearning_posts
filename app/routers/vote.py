from pyexpat import model
from fastapi import FastAPI, HTTPException, responses, status, APIRouter, Depends
from app import schema, models, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Vote"]
)


@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(payload: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == payload.post_id).first()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {payload.post_id} dosen't exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == payload.post_id, models.Vote.user_id == current_user.id)
    found_query = vote_query.first()
    if (payload.vote_dir == "True"):
        if found_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f" User already {current_user.id} already like on post {payload.post_id}")
        new_vote = models.Vote(post_id=payload.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Succesfully added vote"}
    else:
        if not found_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Vote dosen't exist")
        vote_query.delete()
        db.commit()
        return {"Message": "Vote deleted Successfully"}