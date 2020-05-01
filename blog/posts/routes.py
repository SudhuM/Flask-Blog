from flask import Blueprint, render_template, request, redirect, flash, url_for, abort
from flask_login import current_user, login_required
from blog.posts.models import Post
from blog.posts.forms import PostCreationForm, EditPostForm
from blog import db


posts = Blueprint('posts', __name__)


# post creation route
@posts.route('/post', methods=['GET', 'POST'])
@login_required
def post_creation():

    form = PostCreationForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user)

        db.session.add(post)
        db.session.commit()

        flash('Your post has been successfully created.', 'success')
        return redirect(url_for('main.home'))

    return render_template('post_creation.htm', form=form, title='post')


@posts.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)
    form = EditPostForm()
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been successfully updated', 'success')
        return redirect(url_for('main.home'))
    return render_template('editpost.htm', title=post.title, form=form)


@posts.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if not(post) or current_user != post.author:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your Post was successfully deleted.', 'success')
    return redirect(url_for('main.home'))


@posts.route('/post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    '''
    Params : Post id <int>

    Desc : Route to View the posts with the post Id to display the individual post

    '''

    post = Post.query.get(post_id)
    return render_template('viewpost.htm', post=post, title=post.title)


# Route to both the post viewing of an induvidual person
# and also the same route to the post viewing of the current logged in user
