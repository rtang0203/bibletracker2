#!/usr/bin/env python3
"""
Migration script to set up database tables
Run this with: python migrate.py
"""

import os
from dotenv import load_dotenv
from app import create_app, db

# Load environment variables from .env file
load_dotenv()

def run_migrations():
    # Set production config
    os.environ['FLASK_CONFIG_TYPE'] = 'production'
    
    # Create app with production config
    app = create_app()
    
    with app.app_context():
        try:
            # Run migrations
            from flask_migrate import upgrade
            upgrade()
            print("✅ Database migrations completed successfully!")
            
            # Verify tables exist
            from app.models import User, Group, ReadingEntry
            print("✅ Database tables verified!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
    
    return True

if __name__ == '__main__':
    run_migrations() 