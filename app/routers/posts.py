from pyexpat import model
from unittest import result
from fastapi import FastAPI, responses, status, HTTPException, Depends, Response, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import session
from app.database import get_db
from app import models
from app import schema, oauth2

router = APIRouter(
    tags=['posts']
)

@router.get('/posts', response_model=List[schema.GetResponseBackOut])
async def posts(db: session= Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # curr.execute(""" select * from posts """)
    # posts_rec = curr.fetchall()
    print(search)
    posts_rec = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, 
                                        isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    return results

@router.post('/createpost', status_code=status.HTTP_201_CREATED, response_model=schema.ResponceBack  )
async def create_post(payload: schema.CreatePost, db: session= Depends(get_db), user_id: int=Depends(oauth2.get_current_user)):
    # curr.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #             (payload.title, payload.content, payload.publish))

    # new_post = curr.fetchone()
    # conn.commit()
    # new_post = models.Post(title=payload.title, content=payload.content, published=payload.publish)
    print(user_id.id)
    new_post = models.Post(user_id=user_id.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts/{id}", response_model=schema.GetResponseBackOut)
async def get_post(id: int, db: session= Depends(get_db)):
    # curr.execute(""" SELECT * FROM posts WHERE  id = %s""", (str(id),))
    # post = curr.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, 
                                        isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail= f"post not found with the id {id}")
    return post


@router.delete('/delete_post/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: session= Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # curr.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # delete_data = curr.fetchone()
    # conn.commit()
    query = db.query(models.Post).filter(models.Post.id == id)
    delete_post = query.first()
    if delete_post is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"There is No post to delete with the id {id}")
    
    if delete_post.user_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not authorised to delete someone post")
    query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/update_post/{id}", response_model=schema.ResponceBack)
def update_post(id: int, payload: schema.CreatePost, db: session= Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # curr.execute(""" UPDATE posts set title= %s, content=%s WHERE id=%s returning *""", (payload.title, payload.content, str(id),))
    # update_post = curr.fetchone()
    # conn.commit()

    query = db.query(models.Post).filter(models.Post.id == id)
    update_post = query.first()
    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Non post to update with the id {id}")

    if delete_post.user_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not authorised to update someone post")

    query.update(payload.dict())
    db.commit()

    return query.first()
