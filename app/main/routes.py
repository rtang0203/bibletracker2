# app/main/routes.py
from flask import render_template, redirect, url_for
from flask_login import current_user
from . import main_bp

@main_bp.route('/')
def index():
    """Landing page for the application"""
    # If user is already logged in, redirect them to the readings dashboard
    if current_user.is_authenticated:
        return redirect(url_for('readings.index'))
    
    # Otherwise show the landing page
    return render_template('main/index.html', title='Welcome')