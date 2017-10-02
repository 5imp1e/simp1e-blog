# !/usr/bin/evn python
# -*- coding: utf-8 -*-


from flask import current_app, url_for, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
import bleach
from markdown import markdown


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
#   暂时不使用权限功能
#    default = db.Column(db.Boolean, default=False, index=True)
#    permissions = db.Column(db.Integer)
#
#    @staticmethod
#    def insert_roles():
#        roles = {
#            'User': (Permission.COMMENT, True)
#            'Administer': (0xff, False)
#        }

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permission:
    COMMENT = 0x02
    ADMINISTER = 0x80


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    title = db.Column(db.Text, unique=True)
    summary = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=10):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            p = Post(content=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     timestamp=forgery_py.date.date(True),
                     title=forgery_py.lorem_ipsum.sentence(),
                     summary=forgery_py.lorem_ipsum.sentence(),
                     author_id='simp1e')
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1',
                        'h2', 'h3', 'p', 'img']
        attrs = {
            'img': ['src', 'alt']
        }
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, out_format='html'), attributes=attrs,
            tags=allowed_tags, strip=True))


db.event.listen(Post.content, 'set', Post.on_changed_body)
