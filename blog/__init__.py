from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blog.config import Config


# instance of the Database
db = SQLAlchemy()

# instance of Bcrypt
bcrypt = Bcrypt()

# instance of Login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'danger'

# Mail instance
mail = Mail()


# create app factory function
def create_app(config_class=Config):

    # initiating the app with the from_object function to the Config class object

    app = Flask(__name__)

    app.config.from_object(Config)
   # SqlAlchemy database instance

    with app.app_context():
        db.init_app(app)

        # Crypting instance
        bcrypt.init_app(app)

        # Mail server instance configuration
        mail.init_app(app)

        # login Manager instance
        login_manager.init_app(app)

        # routes import from the respective packages
        from blog.users.routes import users
        from blog.posts.routes import posts
        from blog.main.routes import main

        # registering the blue print of the routes.
        app.register_blueprint(users, url_prefix='/users')
        app.register_blueprint(posts, url_prefix='/posts')
        app.register_blueprint(main)

    return app
