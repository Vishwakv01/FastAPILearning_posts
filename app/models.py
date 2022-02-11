from email.mime import base
from tkinter import CASCADE
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False )
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="False", nullable=False)
    created_at = Column(TIMESTAMP(), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(), nullable=False, server_default=text("now()"))
    phoneno = Column(String)


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
