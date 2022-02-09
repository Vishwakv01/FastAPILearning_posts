from fastapi import FastAPI
from app.database import engine 
from app import models
from app.routers import posts, users, auth, vote
from app import config


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def root():
    return {'Message': 'Hello World!!'}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)