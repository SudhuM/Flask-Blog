from flask import (Blueprint, render_template, redirect,
                   request, url_for, flash, abort, session)
from blog.users.forms import (
    RegistrationForm, LoginForm, UpdateForm, RequestResetPasswordForm, ResetPasswordForm)
from blog.users.models import User
from flask_login import current_user, login_user, logout_user, login_required
from blog.users.utils import save_picture, send_password_reset_email
from blog.posts.models import Post
from datetime import timedelta
from blog import db, bcrypt
# db and bcrypy import need to be fixed


users = Blueprint('users', __name__)


# Registration route
@users.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        flash('You have already logged in!', 'info')
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        user = registration_data(form)
        if user:
            flash(
                f'Account {user.username} been successfully created. You can Login', 'success')
            return redirect(url_for('users.login'))

    return render_template('register.htm', form=form, title='register')


# crypt the password and store the details to the Database
def registration_data(form):
    hashed_password = bcrypt.generate_password_hash(
        form.password.data).decode('utf-8')

    user = User(username=str((form.username.data).capitalize()),
                email=form.email.data, password=hashed_password)

    db.session.add(user)
    db.session.commit()

    return user

# login Route
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        flash('You have already logged in!', 'info')
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password_check_status = password_check(form, user)
        if user and password_check_status:
            login_user(user, remember=form.remember_me.data,
                       duration=timedelta(seconds=1800))
            flash('You have successfully logged in.', 'success')

            return redirect(url_for('main.home'))
        elif not(user):
            flash('Incorrect Email Id.Please check.', 'danger')
        elif not(password_check_status):
            flash('Incorrect Password.Please check.', 'danger')

    return render_template('login.htm', title='login', form=form)


def password_check(form, user):
    if user:
        return bcrypt.check_password_hash(user.password, form.password.data)
    return False

# logout route
@users.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out.Please login to continue.', 'warning')
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    information_form = UpdateForm()

    if information_form.validate_on_submit():

        if information_form.profile_picture.data:
            image_file = save_picture(
                information_form.profile_picture.data)

            current_user.profile_pic = image_file

        current_user.username = information_form.username.data
        current_user.email = information_form.email.data

        db.session.commit()
        flash(
            f'Your account has been updated successfully', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        information_form.username.data = current_user.username
        information_form.email.data = current_user.email

    image_file = url_for(
        'static', filename=f'Profile_Pictures/{current_user.profile_pic}')

    return render_template('account.htm', title='Account', image_file=image_file, form=information_form)


@users.route('/account/myposts/<string:username>', methods=['GET'])
def my_posts(username):
    '''
    Params : username <String>

    Desc : Route to view all the post by the individual user
           also route to view the logged in user post in account/profile section

           Sorted out by username param as it has both current_user and also post author as the param

    '''
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    if not(user):
        abort(404)

    else:
        posts = Post.query.filter_by(
            author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('my_posts.htm', posts=posts, username=username)


@users.route('/reset', methods=['GET', 'POST'])
def reset_password_request():
    form = RequestResetPasswordForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        send_password_reset_email(user)
        flash(
            'We have sent an email with the instructions to reset the password.Please check ', 'info')
        return redirect(url_for('users.login'))

    return render_template('request_reset_password.htm', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)

    if not(user):
        flash('The Token Expired or token is invalid', 'warning')
        return redirect(url_for('users.reset_password_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        user.password = hashed_password

        db.session.commit()
        flash('Your password has been successfully updated!You can login now.', 'success')

        return redirect(url_for('users.login'))
    form.email.data = user.email
    return render_template('reset_password.htm', title='Reset Password', form=form)
