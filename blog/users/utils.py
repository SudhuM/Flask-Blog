import secrets
import os
from flask import url_for, current_app
from blog import mail
from flask import current_app
from PIL import Image
from flask_mail import Message


def save_picture(picture):
    random_hex = secrets.token_hex(16)

    _, file_ext = os.path.splitext(picture.filename)

    file_name = random_hex + file_ext

    file_location = os.path.join(
        current_app.root_path, 'static/Profile_Pictures', file_name)

    resized_picture = Image.open(picture)
    size = (180, 180)

    resized_picture.thumbnail(size)
    resized_picture.save(file_location)
    return file_name


def send_password_reset_email(user):
    token = user.generate_reset_token()

    msg = Message('Password Reset Email',
                  sender='noreply@demo.com', recipients=[user.email])

    msg.body = f''' To Reset the password to your account ,please follow the link below

{ url_for('users.reset_password' , token = token , _external = True) }

If you did not request to change the password , please ignore this email,no changes will be applied to your account.
'''

    mail.send(msg)
