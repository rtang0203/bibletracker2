# Flask application initialization 
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import os
import sys

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

login_manager.login_view = 'auth.login'  # Where to redirect if user is not logged in
login_manager.login_message = 'Please log in to access this page.'

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Load configuration based on FLASK_CONFIG_TYPE environment variable
    config_type = os.environ.get('FLASK_CONFIG_TYPE', 'development') # Default to development
    if config_type == 'production':
        app.config.from_object('app.config.ProductionConfig')
    elif config_type == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        # Default to DevelopmentConfig if FLASK_CONFIG_TYPE is invalid and no class is passed
        app.config.from_object('app.config.DevelopmentConfig')

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
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

    from app.main import main_bp
    app.register_blueprint(main_bp)
    
    # Create database tables # REMOVED: db.create_all()
    # with app.app_context():
    #     db.create_all() # This should be handled by Flask-Migrate commands like `flask db upgrade`
    
    return app