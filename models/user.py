from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from models.post import BlogPost
from models.comments import Comment

db = SQLAlchemy()

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

# Configure User
class BlogUser(UserMixin, db.Model):
    __tablename__ = "blog_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(500))
    name: Mapped[str] = mapped_column(String(1000))
    # Relationship between BlogUser and BlogPost
    posts = relationship("BlogPost", back_populates = "author")
    # Relationship between BlogUser and Comments
    comments = relationship("Comment", back_populates = "author")