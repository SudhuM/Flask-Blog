
from blog import db, login_manager
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# user Loader
@login_manager.user_loader
def user_loader(user_id):
    # user_id is a string , so need to be converted to an int
    return User.query.get(int(user_id))

# Database Model Classes


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    profile_pic = db.Column(
        db.String(20), nullable=False, default='default.jpg')

    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email})'

    def generate_reset_token(self, expire_secs=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_secs)
        token = s.dumps({'user_id': self.id}).decode('utf-8')

        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']

        except:
            return None

        return User.query.get(int(user_id))
