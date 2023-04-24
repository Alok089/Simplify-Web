from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, request, g, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
app.app_context().push()
login_manager = LoginManager()
login_manager.init_app(app)
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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

db.create_all()


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=['POST','GET'])
def register():
    register_user = RegisterForm()
    if register_user.validate_on_submit():
        print("attempting validation")
        user = User.query.filter_by(email=register_user.email.data).first()
        if user:
            flash("Look like you have already registered with us, please login using your past credentials")
            return redirect(url_for('login'))
        record = User(email=register_user.email.data,
                       password= generate_password_hash(register_user.password.data, method='pbkdf2:sha256', salt_length=8),
                       name=register_user.name.data)
        db.session.add(record)
        db.session.commit()
        login_user(record)
        return redirect(url_for('get_all_posts'))
    return render_template("register.html", form=register_user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    user_logged_in = LoginForm()
    if user_logged_in.validate_on_submit():
        user = User.query.filter_by(email=user_logged_in.email.data).first()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please register or try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password,user_logged_in.password.data):
            flash("incorrect password, please try again.")
            return redirect(url_for('login'))

        for user in User.query.order_by(User.email).all():
            password_match = check_password_hash(user.password, user_logged_in.password.data)
            if user.email == user_logged_in.email.data and password_match:
                login_user(user)
                return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=user_logged_in)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods = ['POST','GET'])
@login_required
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    comment_feed = Comments.query.filter_by(post_id = post_id)
    comments = CommentForm()
    if comments.validate_on_submit():
        record = Comments(post_id=post_id,
                          commentor_id=current_user.id,
                          comment=comments.comment.data)
        db.session.add(record)
        db.session.commit()
        return render_template("post.html", post=requested_post, form=comments, feed = comment_feed)
    return render_template("post.html", post=requested_post, form=comments, feed = comment_feed)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/new-post", methods= ['POST','GET'])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author_id=current_user.id,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>")
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
