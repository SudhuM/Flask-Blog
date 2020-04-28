from flask_wtf import FlaskForm
from blog.users.models import User
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

# Registration form


class RegistrationForm(FlaskForm):

    username = StringField('UserName', validators=[InputRequired(), DataRequired(),
                                                   Length(min=5, max=20)])

    # user validation
    def validate_username(self, username):
        user = User.query.filter_by(
            username=username.data.capitalize()).first()

        if user:
            raise ValidationError(
                'User name already exists , please choose another one')

    email = StringField('Email', validators=[
        InputRequired(), DataRequired(), Email()])

    # validate Email
    def validate_email(self, email):
        email_id = User.query.filter_by(email=email.data).first()

        if email_id:
            raise ValidationError(
                'Email Id has already been registered.Please choose another one')

    password = PasswordField('Password', validators=[
        InputRequired(), DataRequired(), Length(min=6,  max=15)])

    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), DataRequired(),  EqualTo('password')])

    register = SubmitField('Sign Up')


# Login Form


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[
        InputRequired(), DataRequired(), Email()])

    password = PasswordField('Password', validators=[
        InputRequired(), DataRequired()])

    remember_me = BooleanField('Remember me')

    login = SubmitField('Login')

# User Update Form


class UpdateForm(FlaskForm):
    username = StringField('UserName', validators=[InputRequired(), DataRequired(),
                                                   Length(min=5, max=20)])

    # user validation
    def validate_username(self, username):

        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'User name already exists , please choose another one')

    email = StringField('Email', validators=[
        InputRequired(), DataRequired(), Email()])

    profile_picture = FileField('Update Profie Picture', validators=[
        FileAllowed(['jpg', 'png'])])

    # validate Email
    def validate_email(self, email):

        if email.data != current_user.email:
            email_id = User.query.filter_by(email=email.data).first()
            if email_id:
                raise ValidationError(
                    'Email Id has already been registered.Please choose another one')

    update = SubmitField('Update')


class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[
        InputRequired(), DataRequired(), Email()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if not(user):
            raise ValidationError(
                'We don\'t have this email registered.Please create an account if you don\'t have one')

    send_email = SubmitField('Send Reset Email.')


class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password', validators=[
        InputRequired(), DataRequired(), Length(min=6,  max=15)])

    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), DataRequired(),  EqualTo('password')])

    reset = SubmitField('Reset Password')
