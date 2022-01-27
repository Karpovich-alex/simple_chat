from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, widgets, DateField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Length
from collections import namedtuple
from typing import List
from app import db
from app.dialogs import bp


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Submit')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(FlaskForm):
    string_of_files = ['one\r\ntwo\r\nthree\r\n']
    list_of_files = string_of_files[0].split()
    # create a list of value/description tuples
    files = enumerate(list_of_files)
    example = MultiCheckboxField('Label', choices=files)


User = namedtuple('User', ['id', 'username', 'avatar'])


class TestForm(FlaskForm):
    test = DateField('Date!')


data = [('value_a', 'Value A'), ('value_b', 'Value B'), ('value_c', 'Value C')]


def get_users():
    return [User(1, 'Jonh', 'JONH_AVA'), User(11, 'Nick', 'NICK_AVA'), User(3, 'Viki', 'VIKI_AVA')]


class ExampleForm(FlaskForm):
    # data = get_users()
    # avatars = dict((u.id, u.avatar) for u in data)
    # data = list((u.id, u.username) for u in data)

    users_check_box = SelectMultipleField('Pick Things!',
                                          choices=data,
                                          option_widget=widgets.CheckboxInput(),
                                          widget=widgets.ListWidget(prefix_label=False))

    submit = SubmitField("Create Dialog")

    @classmethod
    def create_form(cls, query):
        users = query.all()
        data = list((u.id, u.username) for u in users)

        class F(cls):
            avatars = dict((u.id, u.avatar(20)) for u in users)
            users_check_box = SelectMultipleField('Pick Things!',
                                                  choices=data,
                                                  option_widget=widgets.CheckboxInput(),
                                                  widget=widgets.ListWidget(prefix_label=False))

            submit = SubmitField("Create Dialog")
        return F()
