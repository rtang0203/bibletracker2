# Group management routes
# app/groups/routes.py
from flask import render_template
from flask_login import login_required
from app.groups import groups_bp

@groups_bp.route('/my-groups')
@login_required
def my_groups():
    return render_template('groups/my_groups.html', title='My Groups')