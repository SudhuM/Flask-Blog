from flask import Blueprint, request, render_template
from blog.posts.models import Post
from flask_login import login_required

main = Blueprint('main', __name__)


# Home page route
@main.route('/home')
@main.route('/')
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
