from fastapi import FastAPI
from app.database import engine 
from app import models
from app.routers import posts, users, auth, vote
from app import config
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#  Basically it'll allow to request from any domain
# In origin we can provide specfic url or * from all domain 
# eg: origins = ["https://www.google.com", "https://www.youtube.com", ]
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():
    return {'Message': 'Hello World!! Welcome to Fastapi Learning'}
