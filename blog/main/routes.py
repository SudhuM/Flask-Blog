from flask import Blueprint, request, render_template, current_app, session
from datetime import timedelta
from blog.posts.models import Post
from flask_login import login_required


main = Blueprint('main', __name__)


@current_app.before_request
def before_request():
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(seconds=1800)
    session.modified = True
    SESSION_REFRESH_EACH_REQUEST = True


# Home page route
@main.route('/')
@main.route('/home')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(per_page=5, page=page)

    return render_template('home.htm', posts=posts, title="Home Page")

# About page route
@main.route('/about')
@login_required
def about():
    return render_template('about.htm', title="About Page")
