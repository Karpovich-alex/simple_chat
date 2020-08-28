from flask import request, redirect, render_template, url_for, current_app, flash
from flask_login import login_required, current_user

from app import db
from app.dialogs import bp
from app.models import User, Dialog, Message
from app.dialogs.forms import MessageForm


@bp.route('/')
@login_required
def dialogs():
    d = current_user.dialogs.order_by(Dialog.last_action_time.desc()).all()
    return render_template('dialogs/dialogs.html', dialogs_list=d)


@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def dialog(id):
    if not current_user.dialogs.filter_by(id=id).all():
        return redirect(url_for('dialogs.dialogs'))

    d = Dialog.get_dialog_by_id(id)
    other_user = None
    if len(d.users) == 2:
        other_user = list(filter(lambda u: u != current_user, d.users))[0]
    if not d:
        flash('You have not gor this dialog')
        return redirect(url_for('dialogs.dialogs'))
    form = MessageForm()
    if form.validate_on_submit():
        d.new_message(sender=current_user, body=form.message.data)
        return redirect(url_for('dialogs.dialog', id=id))
    # user_dialog = Dialog.query.filter_by(id=id).first_or_404()
    msg_list = []
    if d:
        # msg_list = Message.query.filter_by(dialog_id=id).order_by(Message.timestamp_send.desc()).paginate(1, 100, False)
        msg_list = d.messages.order_by(Message.timestamp_send.desc()).paginate(1, 100, False)
    return render_template('dialogs/dialog_window.html', messages_list=msg_list.items, form=form, width=50,
                           recipient=other_user)
