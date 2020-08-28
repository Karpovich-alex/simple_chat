from flask import request, redirect, render_template, url_for, current_app, flash
from flask_login import login_required, current_user

from app import db
from app.dialogs import bp
from app.models import User, Dialog, Message
from app.dialogs.forms import MessageForm


@bp.route('/')
@login_required
def dialogs():
    d = current_user.dialogs.all()
    return render_template('dialogs/dialogs.html', dialogs_list=d)


@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def dialog(id):
    form = MessageForm()
    if form.validate_on_submit():
        msg = Dialog.new_message(dialog_id=id, sender=current_user, body=form.message.data)
        return redirect(url_for('dialogs.dialog', id=id))
    user_dialog = Dialog.query.filter_by(id=id).first_or_404()
    msg_list = []
    if user_dialog:
        msg_list = Message.query.filter_by(dialog_id=id).order_by(Message.timestamp_send.desc()).paginate(1, 10, False)
    return render_template('dialogs/dialog_window.html', messages_list=msg_list.items, form=form)



