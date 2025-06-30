# Database initialization script 
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Group, group_members
from datetime import datetime

def setup_database():
    """Set up the database with initial tables and a test admin user"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables first to ensure a clean slate
        db.drop_all()
        
        # Create tables
        db.create_all()
        
        # Create a test admin user
        admin = User(
            username="admin",
            email="admin@example.com"
        )
        admin.set_password("password123")
        
        # Create a sample group
        sample_group = Group(
            name="Sample Bible Study Group",
            description="A test group for demonstration purposes",
            created_by=1,  # Will be the admin user's ID after commit
            is_data_public=True
        )
        
        # Add objects to session and commit to get IDs
        db.session.add(admin)
        db.session.commit()
        
        # Now add the group (admin's ID is now available)
        sample_group.created_by = admin.id
        db.session.add(sample_group)
        db.session.commit()
        
        # Add admin as a member and group admin
        admin.groups.append(sample_group)
        
        # Update the is_admin status in the association table
        stmt = group_members.update().where(
            (group_members.c.user_id == admin.id) & 
            (group_members.c.group_id == sample_group.id)
        ).values(is_admin=True)
        
        db.session.execute(stmt)
        db.session.commit()
        
        print(f"Database initialized with admin user (ID: {admin.id}) and sample group (ID: {sample_group.id})")
        print(f"Sample group code: {sample_group.group_code}")

if __name__ == "__main__":
    setup_database()