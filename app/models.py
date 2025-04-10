# Database models 

from datetime import datetime, date
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import db  # Import db from app package

# Helper table for many-to-many relationship between users and groups
group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow),
    db.Column('is_admin', db.Boolean, default=False)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    groups = db.relationship('Group', secondary=group_members, 
                            backref=db.backref('members', lazy='dynamic'))
    reading_entries = db.relationship('ReadingEntry', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    group_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_data_public = db.Column(db.Boolean, default=True)
    
    # Foreign Keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by])
    reading_entries = db.relationship('ReadingEntry', backref='group', lazy=True)
    
    def generate_group_code(self):
        # Generate a short, random code for joining the group
        return str(uuid.uuid4())[:8].upper()
    
    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        if not self.group_code:
            self.group_code = self.generate_group_code()
    
    def __repr__(self):
        return f'<Group {self.name}>'
    
    @property
    def member_count(self):
        return self.members.count()

class ReadingEntry(db.Model):
    __tablename__ = 'reading_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False)
    has_read = db.Column(db.Boolean, default=False)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    
    # Composite unique constraint to ensure one entry per user per group per day
    __table_args__ = (
        db.UniqueConstraint('user_id', 'group_id', 'date', name='unique_daily_reading'),
    )
    
    def __repr__(self):
        read_status = "Read" if self.has_read else "Not Read"
        return f'<ReadingEntry {self.user_id} - {self.date}: {read_status}>'