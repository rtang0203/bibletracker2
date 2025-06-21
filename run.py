# Application entry point 
from dotenv import load_dotenv
import os

# Load .env.development.local for local development with production DB, otherwise load .env
if os.path.exists('.env.development.local'):
    load_dotenv(dotenv_path='.env.development.local')
else:
    load_dotenv()

from app import create_app
import os # Import os to check environment variables

# Create app instance. Configuration will be loaded based on FLASK_CONFIG_TYPE in create_app.
app = create_app()

# For Vercel serverless functions
if __name__ == '__main__':
    # The DEBUG variable from the loaded config will control the debug mode.
    # For local development, you might set FLASK_CONFIG_TYPE=development (or leave it unset)
    # and app.config['DEBUG'] will be True.
    # For local testing of production settings, set FLASK_CONFIG_TYPE=production,
    # and app.config['DEBUG'] will be False.
    app.run(debug=app.config.get('DEBUG', True)) # Use debug from config, default to True if not set for safety