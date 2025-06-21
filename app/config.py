# Configuration settings 
import os

class Config:
    """Base config class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bible_reading_app.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Railway automatically provides DATABASE_URL when you add a PostgreSQL service
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # Ensure DATABASE_URL is set in production, otherwise the app will fail to start, which is intended.