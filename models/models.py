from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text

db = SQLAlchemy()

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_users.id"))
    # Relationship between BlogPost and BlogUser
    author = relationship("BlogUser", back_populates = "posts")

    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # Relationship between BlogPost and Comments
    comments = relationship("Comment", back_populates = "parent_post")

    def to_dict(self):
        
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
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
    
class Comment(db.Model):
    __tablename__ = "blog_comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_users.id"))
    # Relationship between Comments and User
    author = relationship("BlogUser", back_populates = "comments")
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    # Relationships between Comments and Post
    parent_post = relationship("BlogPost", back_populates="comments")
    text: Mapped[str] = mapped_column(Text, nullable = False)