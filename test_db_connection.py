#!/usr/bin/env python3
"""
Test script to verify production database connection
Run this with: python test_db_connection.py
"""

import os
from dotenv import load_dotenv
from app import create_app, db

def test_connection():
    # Load environment variables
    load_dotenv()
    
    # Set production config for testing
    os.environ['FLASK_CONFIG_TYPE'] = 'production'
    
    # Create app with production config
    app = create_app()
    
    with app.app_context():
        try:
            # Test the connection using modern SQLAlchemy syntax
            with db.engine.connect() as conn:
                conn.execute(db.text('SELECT 1'))
            print("✅ Database connection successful!")
            print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Test if we can create tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    return True

if __name__ == '__main__':
    test_connection() 