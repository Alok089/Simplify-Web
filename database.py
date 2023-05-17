from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin

db = SQLAlchemy()

##CONFIGURE TABLES
class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    comment = db.Column(db.Text, nullable=False)
    commentor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog = relationship("BlogPost", back_populates="comments")
    commentor = relationship("User", back_populates="comments")

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author = relationship("User", back_populates="posts")
    comments = relationship("Comments", back_populates="blog")

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comments", back_populates="commentor")

class Attribute(db.Model):
    __tablename__ = "attributes"
    attribute_id = db.Column(db.Integer, primary_key=True)
    attribute = db.Column(db.String(100))
    value = db.Column(db.String(1000))
    item_id = db.Column(db.String(100))
    item_analyzed_on = db.Column(db.Date)

class Inference_Attributes(db.Model):
    __tablename__ = "inference_attributes"
    attribute_id = db.Column(db.Integer, primary_key=True)
    attribute = db.Column(db.String(100))
    value = db.Column(db.String(1000))
    item_id = db.Column(db.String(100))

class Inference_Categroies(db.Model):
    __tablename__ = "inference_categories"
    category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    value = db.Column(db.String(1000))

class Inference_Association(db.Model):
    __tablename__ = "inference_association"
    association_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)