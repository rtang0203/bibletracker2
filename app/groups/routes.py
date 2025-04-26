# Group management routes

# app/groups/routes.py
from datetime import date # Add date import
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.groups import groups_bp
from app.models import Group, User, group_members, ReadingEntry # Add ReadingEntry import
from .forms import CreateGroupForm, JoinGroupForm # Use relative import
from ..readings.forms import EmptyForm # Import EmptyForm

@groups_bp.route('/my-groups')
@login_required
def my_groups():
    user_groups = current_user.groups
    return render_template('groups/my_groups.html', title='My Groups', groups=user_groups)

@groups_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_group():
    # from app.groups.forms import CreateGroupForm # Removed import from here
    form = CreateGroupForm()
    if form.validate_on_submit():
        group = Group(
            name=form.name.data,
            description=form.description.data,
            created_by=current_user.id,
            is_data_public=form.is_data_public.data
        )
        db.session.add(group)
        db.session.commit()
        
        # Add the creator as a member and admin
        current_user.groups.append(group)
        
        # Update the association table to set is_admin=True
        stmt = group_members.update().where(
            (group_members.c.user_id == current_user.id) & 
            (group_members.c.group_id == group.id)
        ).values(is_admin=True)
        
        db.session.execute(stmt)
        db.session.commit()
        
        flash(f'Group "{group.name}" created successfully! Group code: {group.group_code}')
        return redirect(url_for('groups.view_group', group_id=group.id))
    
    return render_template('groups/create_group.html', title='Create Group', form=form)

@groups_bp.route('/join', methods=['GET', 'POST'])
@login_required
def join_group():
    # from app.groups.forms import JoinGroupForm # Removed import from here
    form = JoinGroupForm()
    if form.validate_on_submit():
        group = Group.query.filter_by(group_code=form.group_code.data.upper()).first()
        
        # Check if user is already a member
        if group in current_user.groups:
            flash('You are already a member of this group.')
            return redirect(url_for('groups.view_group', group_id=group.id))
        
        # Add user to group
        current_user.groups.append(group)
        db.session.commit()
        
        flash(f'You have successfully joined "{group.name}"!')
        return redirect(url_for('groups.view_group', group_id=group.id))
    
    return render_template('groups/join_group.html', title='Join Group', form=form)

@groups_bp.route('/view/<int:group_id>')
@login_required
def view_group(group_id):
    group = Group.query.get_or_404(group_id)
    today = date.today()
    reading_status = {}
    can_see_reading_status = False
    
    # Form for the leave group button
    leave_form = EmptyForm()
    
    # Check if user is a member of this group
    if group not in current_user.groups:
        flash('You are not a member of this group.')
        return redirect(url_for('groups.my_groups'))
    
    # Check if user is an admin of this group (needed for displaying status)
    is_admin = db.session.query(group_members).filter(
        group_members.c.user_id == current_user.id,
        group_members.c.group_id == group.id,
        group_members.c.is_admin == True
    ).first() is not None
    
    # Determine if user can see reading status
    if is_admin or group.is_data_public:
        can_see_reading_status = True
        # Get all entries for today for this group
        today_entries = ReadingEntry.query.filter_by(
            group_id=group_id,
            date=today
        ).all()
        # Create a dictionary of user_id: has_read
        reading_status = {entry.user_id: entry.has_read for entry in today_entries}
    
    return render_template('groups/view_group.html', 
                          title=group.name, 
                          group=group, 
                          is_admin=is_admin, # Still useful for other potential admin actions
                          can_see_reading_status=can_see_reading_status,
                          reading_status=reading_status,
                          today=today,
                          User=User,
                          leave_form=leave_form) # Pass leave_form to template

@groups_bp.route('/leave/<int:group_id>', methods=['POST'])
@login_required
def leave_group(group_id):
    group = Group.query.get_or_404(group_id)
    
    # Can't leave if you're the creator
    if group.created_by == current_user.id:
        flash('As the group creator, you cannot leave the group.')
        return redirect(url_for('groups.view_group', group_id=group.id))
    
    # Remove user from group
    if group in current_user.groups:
        current_user.groups.remove(group)
        db.session.commit()
        flash(f'You have left "{group.name}".')
    
    return redirect(url_for('groups.my_groups'))