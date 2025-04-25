# Reading tracking routes
# app/readings/routes.py
from flask import render_template
from flask_login import login_required
from . import readings_bp

@readings_bp.route('/')
@login_required
def index():
    return render_template('readings/index.html', title='My Reading Tracker')