#!/usr/bin/env python
#-*- coding:utf-8 -*-

import hashlib
import uuid

from flask.ext.login import UserMixin

from sigmago.corelib.ext import db


class UserAccount(UserMixin, db.Model):
    """The account model of register user."""

    #: the strategy to generate hash salt
    hash_salt_generator = staticmethod(lambda: uuid.uuid4().hex)
    #: the strategy to hash password
    hash_algorithm = "sha256"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(255), unique=True)
    nickname = db.Column(db.Unicode(30), unique=True)
    passwd_salt = db.Column(db.String(32), nullable=False)
    passwd_hash = db.Column(db.String(64), nullable=False)

    def __init__(self, **fields):
        #: use a random password by default
        passwd = fields.pop("passwd", self.hash_salt_generator())
        #: update password
        self.change_passwd(passwd)
        #: assign other attributes
        super(UserAccount, self).__init__(**fields)

    def change_passwd(self, new_passwd):
        """Changes a new password.

        The password salt will be updated.
        """
        #: generate a new salt
        self.passwd_salt = self.hash_salt_generator()
        #: change the password hash value
        self.passwd_hash = self.make_passwd_hash(new_passwd)

    def check_passwd(self, input_passwd):
        """Checks is a input password correct.

        A boolean value will be return which equals true for correct and false
        for wrong.
        """
        #: calculate the input password hash value
        input_passwd_hash = self.make_passwd_hash(input_passwd)
        #: not empty and be same
        return self.passwd_hash and self.passwd_hash == input_passwd_hash

    def make_passwd_hash(self, raw_passwd):
        """Creates a hash value from a raw password string."""
        #: TODO use werkzeug's hash algorithm instead this
        hashobj = hashlib.new(self.hash_algorithm)
        hashobj.update('%s:%s' % (self.passwd_salt, raw_passwd))
        return hashobj.hexdigest()


def get_user_by_id(uid):
    """Accept a string user id and return a account object."""
    if uid.isdigit():
        return UserAccount.query.get(int(uid))
    else:
        return UserAccount.query.filter_by(name=uid).one()
