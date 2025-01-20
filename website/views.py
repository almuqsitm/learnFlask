from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import pytz
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    # Convert note dates to Eastern Standard Time (EST)
    est_tz = pytz.timezone('America/New_York')
    notes = []
    for note in current_user.notes:
        est_date = note.date.astimezone(est_tz)
        formatted_date = est_date.strftime('%Y-%m-%d %H:%M:%S')
        notes.append({'data': note.data, 'date': formatted_date, 'id': note.id})

    return render_template("home.html", user=current_user, notes=notes)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})