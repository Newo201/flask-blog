# Flask imports
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, abort
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from datetime import datetime
# Authentication
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
# Databases
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey
# Custom Imports
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.post import PostForm
from forms.comment import CommentForm
from models.models import BlogUser, BlogPost, Comment

# from models import Base, BlogPost
# Misc imports
from datetime import datetime
from dotenv import load_dotenv
import os

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Access environment variables to connect to database
pg_user = os.environ.get('PG_USER')
pg_password = os.environ.get('PG_PASSWORD')
pg_host = os.environ.get('PG_HOST')
pg_databse = os.environ.get('PG_DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_databse}'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
# Initialise other flask components
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap5(app)
Gravatar = Gravatar(app)

# User Loader Callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(BlogUser, user_id)

def user_already_exists(email):
    current_user = db.session.execute(db.select(BlogUser).where(BlogUser.email == email))
    if current_user.scalar():
        return True
    return False

def admin_user_required(func):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.id == 1:
                return func(*args, **kwargs)
        else:
            abort(code = 403)
    return wrapper

@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    all_blogs = result.scalars().all()
    return render_template("index.html", all_posts=all_blogs)

# TODO: Add a route so that you can click on individual posts.
@app.route('/post/<int:post_id>', methods = ['GET', 'POST'])
def show_post(post_id):
    form = CommentForm()
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    result = db.session.execute(db.select(Comment).where(Comment.post_id == post_id))
    if result:
        try:
            comments = result.scalars().all()
        except TypeError:
            comments = [result.scalar()]
        print(comments)
    else:
        comments = None
    if form.validate_on_submit():
        new_comment = Comment(author_id = current_user.id, post_id = post_id, text = form.comment.data)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(f"/post/{post_id}")
    return render_template("post.html", post=requested_post, comments = comments, form = form)


# TODO: add_new_post() to create a new blog post
@app.route("/new", methods = ['GET', 'POST'], endpoint = 'new_post')
@admin_user_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        body = form.body.data
        img_url = form.img_url.data
        date = datetime.today().strftime("%A %d, %Y")
        new_post = BlogPost(title = title, subtitle = subtitle, author_id = current_user.id, 
                            body = body, img_url = img_url, date = date)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/")
    return render_template("make-post.html", form = form)

# TODO: edit_post() to change an existing blog post
@app.route("/edit-post/<int:post_id>", endpoint = 'edit_post')
@admin_user_required
def edit_post(post_id):
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    form = PostForm(
        title = post.title,
        subtitle = post.subtitle,
        name = post.author.name,
        img_url = post.img_url,
        body = post.body
    )
    return render_template("make-post.html", form = form, editing = True)

# TODO: delete_post() to remove a blog post from the database
@app.route("/delete-post/<int:post_id>", endpoint = 'delete_post')
@admin_user_required
def delete_post(post_id):
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    db.session.delete(post)
    db.session.commit()
    return redirect("/")

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Securely store the password
        email = form.email.data
        password = form.password.data
        # Give an error if the user did not enter a correct email
        if not user_already_exists(email):
            flash("Invalid credentials, please try again", category = 'error')
            return render_template("login.html", form = form)
        user_to_check = db.session.execute(db.select(BlogUser).where(BlogUser.email == email)).scalar()
        # If the user entered the incorrect password
        # As an extension could find a way of limiting the number of password attempts
        if not check_password_hash(user_to_check.password, password):
            flash("Invalid credentials, please try again", category = 'error')
            return render_template("login.html", form = form)
        # Login the user
        login_user(user_to_check)
        return redirect("/")
    return render_template("login.html", form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Securely store the password
        hashed_password = generate_password_hash(form.password.data, method = "pbkdf2")
        name = form.name.data
        email = form.email.data
        # Give an error if the user already exists
        if user_already_exists(email):
            flash("Invalid credentials, please try again", category = 'error')
            return render_template("register.html", form = form)
        else:
            new_user = BlogUser(email = email, password = hashed_password, name = name)
            db.session.add(new_user)
            db.session.commit()
            # Login the user
            login_user(new_user)
            return redirect("/")
    return render_template("register.html", form = form)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
