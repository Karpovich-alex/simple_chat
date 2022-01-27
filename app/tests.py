#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Dialog, Message
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='test_user')
        u.set_password('cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    # def test_friend(self):
    #     u1 = User(username='First')
    #     u2 = User(username='Second')
    #     u1.add_to_friend(u2)


class DialogModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_users(self):
        self.u1 = User(username='User1')
        self.u2 = User(username='User2')
        self.u3 = User(username='User3')
        db.session.add_all([self.u1, self.u2, self.u3])
        db.session.commit()

        self.u1 = User.query.filter_by(id=1).first()
        self.u2 = User.query.filter_by(id=2).first()
        self.u3 = User.query.filter_by(id=3).first()

    def test_create(self):
        self.create_users()
        d = Dialog.create_dialog(self.u1, self.u2)
        self.assertIs(Dialog.query.filter_by(id=1).first(), d)

    def create_dialog(self, u1, u2, **kwargs):
        d = Dialog(users=[u1, u2], **kwargs)
        db.session.add(d)
        db.session.commit()
        return d

    def test_create_dialog_ids(self):
        self.create_users()
        d = Dialog.create_dialog_new(ids=(1, 2, 3))
        self.assertEqual(d, Dialog.get_by_id(1))

    def test_check_dialog(self):
        self.create_users()
        self.create_dialog(self.u1, self.u2)
        self.assertTrue(Dialog.has_dialog(self.u1, self.u2))
        self.assertFalse(Dialog.has_dialog(self.u1, self.u3))

    def test_get_dialog(self):
        self.create_users()

        d = Dialog.get_dialog(self.u1, self.u2)
        self.assertEqual(1, d.id)
        self.assertIsNot(d, Dialog.get_dialog(self.u1, self.u3))
        self.assertIs(d, Dialog.get_dialog(self.u1, self.u2))
        self.assertEqual(d.id, Dialog.get_dialog(self.u1, self.u2).id)

    def test_get_info(self):
        self.create_users()
        self.create_dialog(self.u1, self.u2, dialog_name='First_dialog')
        self.assertEqual(Dialog.get_dialog_info(self.u1, self.u2, info='id'), 1)
        self.assertEqual(Dialog.get_dialog_info(self.u1, self.u2, info='dialog_name'), 'First_dialog')

    def test_get_by_id(self):
        self.create_users()
        d = self.create_dialog(self.u1, self.u2)
        d1 = self.create_dialog(self.u1, self.u3)
        self.assertIs(d, Dialog.get_by_id(1))
        self.assertIsNot(d, Dialog.get_by_id(2))

    def test_get_rece(self):
        self.create_users()
        d = self.create_dialog(self.u1, self.u2)
        self.assertIs(d.get_recipients(self.u1)[0], self.u2)
        self.assertIs(d.get_recipients(self.u2)[0], self.u1)

    def test_dialog_name(self):
        self.create_users()
        d = self.create_dialog(self.u1, self.u2)
        self.assertEqual(d.get_dialog_name(self.u1), self.u2.username)


class MessageModelTest(unittest.TestCase):
    def create_users(self):
        self.u1 = User(username='User1')
        self.u2 = User(username='User2')
        self.u3 = User(username='User3')
        db.session.add_all([self.u1, self.u2, self.u3])
        db.session.commit()
        self.d = self.create_dialog(self.u1, self.u2)
        self.d1 = self.create_dialog(self.u1, self.u3)

    def create_dialog(self, u1, u2, **kwargs):
        d = Dialog(users=[u1, u2], **kwargs)
        db.session.add(d)
        db.session.commit()
        return d

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.create_users()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_message(self):
        msg = self.d.new_message(sender=self.u1, body='text_body')
        self.assertTrue(Message.query.filter_by(id=1).first_or_404())
        self.assertIs(msg, Message.query.filter_by(id=1).first_or_404())
        self.assertEqual(Message.query.filter_by(id=1).first().body, 'text_body')
        self.assertIs(Dialog.get_by_id(1).last_message, msg)
        self.assertIsNot(Dialog.get_by_id(2).last_message, msg)

    def test_last_message(self):
        msg = self.d.new_message(sender=self.u1, body='text_body')
        self.assertIs(msg, self.d.last_message)


if __name__ == '__main__':
    unittest.main(verbosity=2)
