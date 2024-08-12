from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from models.comments import Comment
from models.user import BlogUser

db = SQLAlchemy()

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

# CONFIGURE TABLE
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
    
# with app.app_context():
#     db.create_all()

# # Initial Blog Posts
# with app.app_context():
#     first_blog = BlogPost(title = "Example Post", 
#                           subtitle = "Check out my example",
#                           date = "August 7th, 2024",
#                           body = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
#                           sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
#                           Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi 
#                           ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
#                           in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
#                           Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt 
#                           mollit anim id est laborum.""",
#                           author = "Owen Jackson",
#                           img_url = "https://tse1.mm.bing.net/th?id=OIP._t5PwJneEsl0m0qJW7PoUgHaEK&pid=Api&P=0&h=180")
#     db.session.add(first_blog)
#     db.session.commit()