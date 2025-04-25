# Flask application initialization 
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Where to redirect if user is not logged in
login_manager.login_message = 'Please log in to access this page.'

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import models and register user loader AFTER initializing extensions
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints AFTER initializing extensions and defining models
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.groups import groups_bp
    app.register_blueprint(groups_bp)
    
    from app.readings import readings_bp
    app.register_blueprint(readings_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app