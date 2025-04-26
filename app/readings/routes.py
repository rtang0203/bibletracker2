# Reading tracking routes
# app/readings/routes.py
from datetime import date, timedelta
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from ..models import ReadingEntry, Group, group_members
from . import readings_bp
from .forms import DailyReadingForm, EmptyForm
from flask_wtf.csrf import generate_csrf # Needed for CSRF token in the template

@readings_bp.route('/')
@login_required
def index():
    """Main reading tracker dashboard"""
    # Get user's groups
    user_groups = current_user.groups
    
    # Get today's date
    today = date.today()
    
    # Get reading entries for the current user for today
    today_entries = ReadingEntry.query.filter_by(
        user_id=current_user.id,
        date=today
    ).all()
    
    # Create a dictionary of group_id: reading_entry
    today_readings = {entry.group_id: entry for entry in today_entries}
    
    # Create instance of the empty form for the "Mark All Read" button
    mark_all_form = EmptyForm()
    
    return render_template('readings/index.html', 
                          title='My Reading Tracker',
                          user_groups=user_groups,
                          today_readings=today_readings,
                          today=today,
                          mark_all_form=mark_all_form)

@readings_bp.route('/mark/<int:group_id>', methods=['GET', 'POST'])
@login_required
def mark_reading(group_id):
    """Mark daily reading for a specific group"""
    group = Group.query.get_or_404(group_id)
    
    # Check if user is member of this group
    if group not in current_user.groups:
        flash('You are not a member of this group.')
        return redirect(url_for('readings.index'))
    
    today = date.today()
    
    # Check if entry already exists for today
    entry = ReadingEntry.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        date=today
    ).first()
    
    if not entry:
        # Create new entry if none exists
        entry = ReadingEntry(
            user_id=current_user.id,
            group_id=group_id,
            date=today,
            has_read=False
        )
        db.session.add(entry)
    
    form = DailyReadingForm()
    
    if form.validate_on_submit():
        entry.has_read = form.has_read.data
        db.session.commit()
        flash('Reading status updated successfully!')
        return redirect(url_for('readings.index'))
    
    # Pre-populate form with current values
    form.has_read.data = entry.has_read
    
    return render_template('readings/mark_reading.html', 
                          title='Update Reading Status',
                          form=form, 
                          group=group)

@readings_bp.route('/history/<int:group_id>')
@login_required
def reading_history(group_id):
    """View reading history for a specific group"""
    group = Group.query.get_or_404(group_id)
    
    # Check if user is member of this group
    if group not in current_user.groups:
        flash('You are not a member of this group.')
        return redirect(url_for('readings.index'))
    
    # Get dates for the last 30 days
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    # Query for all entries in this group between start and end date
    entries = ReadingEntry.query.filter(
        ReadingEntry.group_id == group_id,
        ReadingEntry.date >= start_date,
        ReadingEntry.date <= end_date
    ).all()
    
    # Check if user can see everyone's data or just their own
    is_admin = db.session.query(group_members).filter(
        group_members.c.user_id == current_user.id,
        group_members.c.group_id == group_id,
        group_members.c.is_admin == True
    ).first() is not None
    
    can_see_all = is_admin or group.is_data_public
    
    if not can_see_all:
        # Filter to only show current user's entries
        entries = [e for e in entries if e.user_id == current_user.id]
    
    # Organize entries by date and user
    entries_by_date = {}
    for entry in entries:
        if entry.date not in entries_by_date:
            entries_by_date[entry.date] = []
        entries_by_date[entry.date].append(entry)
    
    return render_template('readings/history.html',
                          title=f"Reading History - {group.name}",
                          group=group,
                          entries_by_date=entries_by_date,
                          can_see_all=can_see_all)

@readings_bp.route('/mark-all-today', methods=['POST'])
@login_required
def mark_all_read():
    """Mark all of current user's groups as read for today."""
    form = EmptyForm() # Instantiate the form
    # Validate the form (this performs the CSRF check)
    if form.validate_on_submit(): 
        today = date.today()
        user_groups = current_user.groups

        if not user_groups:
            flash("You are not a member of any groups.")
            return redirect(url_for('readings.index'))

        # Fetch existing entries for today to optimize updates
        existing_entries = ReadingEntry.query.filter(
            ReadingEntry.user_id == current_user.id,
            ReadingEntry.date == today,
            ReadingEntry.group_id.in_([g.id for g in user_groups])
        ).all()
        
        entries_dict = {entry.group_id: entry for entry in existing_entries}
        
        new_entries_added = False
        entries_updated = False

        for group in user_groups:
            entry = entries_dict.get(group.id)
            if entry:
                if not entry.has_read:
                    entry.has_read = True
                    entries_updated = True
            else:
                new_entry = ReadingEntry(
                    user_id=current_user.id,
                    group_id=group.id,
                    date=today,
                    has_read=True
                )
                db.session.add(new_entry)
                new_entries_added = True

        if new_entries_added or entries_updated:
            try:
                db.session.commit()
                flash('All groups marked as read for today!')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {e}', 'danger')
        else:
            flash('All groups were already marked as read for today.')
    else:
        # Handle CSRF validation failure
        flash('Invalid request. Please try again.', 'danger')
            
    return redirect(url_for('readings.index'))