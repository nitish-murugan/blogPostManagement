from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

db = SQLAlchemy()
db_name = "database.db"

def createApp():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secretKey"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    UPLOAD_FOLDER = 'website\static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    db.init_app(app)
    from .view import view
    from .auth import auth
    app.register_blueprint(view,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    from .model import User,Post,Comment
    createDatabase(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def createDatabase(app):
    with app.app_context():
        if not path.exists("website/"+db_name):
            db.create_all()
            print("DB created")
    