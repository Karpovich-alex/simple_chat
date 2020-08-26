from datetime import datetime
from app import current_app, db, login
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inviter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_inviter_friend = db.Column(db.Boolean, default=False)
    invited_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_invited_friend = db.Column(db.Boolean, default=False)
    invite_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    accept_time = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return '<Friends {} and {} is {}>'.format(self.inviter_id, self.invited_id,
                                                  self.is_inviter_friend and self.is_invited_friend)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    dialog_id = db.Column(db.Integer, db.ForeignKey('dialog.id'))

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.relationship('User', backref='message')

    body = db.Column(db.String(140))

    timestamp_send = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    timestamp_read = db.Column(db.DateTime, index=True, default=None)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Dialog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), default='')

    participants_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    messages = db.relationship('Message', backref='dialog')
    last_action_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_message_id = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Dialog {}>'.format(self.id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # friend = db.relationship('Friend', secondary=Friend, primaryjoin=(Friend.c.inviter_id == id),
    #                          secondaryjoin=(Friend.invited_id == id),
    #                          backref=db.backref('Friend', lazy='dynamic'), lazy='dynamic')
    dialogs = db.relationship('Dialog', backref='participant', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def add_friend(self, user):
        if not self.is_friends:
            friend = Friend(inviter_id=self.id, invited_id=user.id)
            db.session.add(friend)
            db.session.commit()

    def delete_from_friend(self, user):
        pass

    def is_friends(self, user):
        return self.friend.filter_by(is_friend=True).filter(
            Friend.c.inviter_id == user.id).count() > 0 or self.friend.filter_by(is_friend=True).filter(
            Friend.c.invited_id == user.id).count() > 0


@login.user_loader
def load_user(id):
    return User.query.get(int(id))