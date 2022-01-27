from flask import request, redirect, render_template, url_for, current_app, flash, g
from flask_login import login_required, current_user

from app import db
from app.dialogs import bp
from app.models import User, Dialog, Message
from app.dialogs.forms import MessageForm, SimpleForm, TestForm, ExampleForm


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

    d: Dialog = Dialog.get_by_id(id)

    other_users = d.get_recipients(current_user)
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
                           recipients=other_users)

@bp.route('/create_dia',methods=['GET','POST'])
def create_dialog():
    try:
        form = g.create_dialog_form
    except AttributeError:
        g.create_dialog_form = ExampleForm.create_form(current_user.query.filter(User.id !=current_user.id).order_by(User.username))
        form = g.create_dialog_form

    if request.method == 'POST':
        print('Submit')
        print(form.users_check_box.data)
        d = Dialog.create_dialog_new(ids=form.users_check_box.data)
        d.users.append(current_user)
        del g.create_dialog_form

        return redirect(url_for('dialogs.dialog', id=d.id))
    print(request.form)
    return render_template('dialogs/new_dialog.html', form=form)


@bp.route('/test', methods=['GET', 'POST'])
def test():
    form = ExampleForm()
    if form.validate_on_submit():
        print(form.users_check_box.data)
        return 'YES'
    return render_template('dialogs/example.html', form=form, User=User)
