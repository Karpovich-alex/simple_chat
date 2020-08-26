from flask import request, render_template, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from app.main import bp
from app.models import User
from app import db
from app.main.forms import EditProfileForm

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    user_list = db.session.query(User).filter(User.id != current_user.id).paginate(1, 10, False)
    if len(user_list.items)==0:
        flash('Sorry, server is empty')
    return render_template('index.html', user_list=user_list.items)


@bp.route('/search')
def search():
    return render_template('search.html')

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)