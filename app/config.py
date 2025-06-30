# Configuration settings 
import os
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# Get the absolute path of the instance folder
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(os.path.dirname(basedir), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

class Config:
    """Base config class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "bible_reading_app.db")}'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Use Vercel Postgres URL if available, otherwise fall back to a general DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')

    if SQLALCHEMY_DATABASE_URI:
        # Correct the database scheme for SQLAlchemy
        if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

        # Providers like Supabase add extra, unsupported parameters to the connection
        # string. We parse the URL and remove them to prevent 'invalid dsn' errors.
        parsed_url = urlparse(SQLALCHEMY_DATABASE_URI)
        query_params = parse_qs(parsed_url.query)
        
        # Filter out any problematic parameters.
        filtered_params = {
            k: v for k, v in query_params.items() if not k.startswith('supa')
        }
        
        new_query = urlencode(filtered_params, doseq=True)
        SQLALCHEMY_DATABASE_URI = urlunparse(parsed_url._replace(query=new_query))
    
    # Ensure a database URL is set in production
    # Ensure DATABASE_URL is set in production, otherwise the app will fail to start, which is intended.