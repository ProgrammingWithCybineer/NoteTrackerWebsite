from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import  login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)

@views.route("/", methods = ["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is to short!", category = "error")
        
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added", category="success")

    return render_template("home.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get("note.Id")
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit
    return jsonify({})


@views.route("/delete-user", methods=["POST"])
def delete_user():
    user = json.loads(request.data)
    user.id = user["email"]
    user = user.query.get("email")
    if user:
        if user.user_id == current_user.id:
            db.session.delete(email=user)
            db.session.commit
    return jsonify({})
