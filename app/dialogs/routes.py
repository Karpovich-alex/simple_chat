from flask import request, redirect, render_template, url_for, current_app, flash

from app import db
from app.dialogs import bp
from app.models import User, Dialog

@bp.route('/dialogs')
def dialogs():
    return render_template('dialogs/dialogs.html')

@bp.route('/dialogs/<int:id>')
def dialog(id):
    pass

@bp.route('/send_message/<username>')
def send_message(username):
    user = User.query.filter_by(username=username)
