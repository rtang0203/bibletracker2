# Flask application initialization 
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    
    # Register blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.groups.routes import groups_bp
    app.register_blueprint(groups_bp)
    
    from app.readings.routes import readings_bp
    app.register_blueprint(readings_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app