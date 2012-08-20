#!/usr/bin/env python
#-*- coding:utf-8 -*-

import hashlib
import uuid

from flask.ext.login import UserMixin

from sigmago.corelib.ext import db, login_manager


class UserAccount(UserMixin, db.Model):
    """The account model of register user."""

    #: the strategy to generate hash salt
    hash_salt_generator = staticmethod(lambda: uuid.uuid4().hex)
    #: the strategy to hash password
    hash_algorithm = "sha256"

    #: available status of user account
    STATUS = ("unactivated", "normal", "banned", "removed")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(255), unique=True)
    nickname = db.Column(db.Unicode(30), unique=True)
    passwd_salt = db.Column(db.String(32), nullable=False)
    passwd_hash = db.Column(db.String(64), nullable=False)
    status = db.Column(db.Enum(*STATUS, name="UserAccountStatus"),
                       nullable=False, default="unactivated")

    @db.validates("name")
    @db.validates("email")
    def validate_to_lower(self, key, value):
        return value.lower()

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

    def is_active(self):
        """Tells me the user is active or not.

        This method implemented the UserMixin's abstract calling.
        """
        return self.status == "normal"

    def ban(self):
        """Ban this account."""
        self._transform_status(["normal"], "banned")

    def remove(self):
        """Remove this account."""
        self._transform_status(["unactivated", "normal"], "removed")

    def activate(self):
        """Activate this account."""
        self._transform_status(["unactivated"], "normal")

    def _transform_status(self, expected_statuses, new_status):
        """Transform this account's status."""
        if self.status == expected_statuses:
            self.status = new_status
        else:
            raise UserStatusError(expected_statuses=expected_statuses,
                                  actually_status=self.status)


class UserStatusError(Exception):
    """Meets an unexpected status transformation in an account."""

    DEFAULT_MESSAGE = ("Only {expected_status} status could be transformed "
                       "to '{target_status}' status, not '{actually_status}'.")

    def __init__(self, message=None, expected_statuses=None,
                 actually_status=None, target_status=None):
        message = message or self.DEFAULT_MESSAGE.format(**locals())
        super(UserStatusError, self).__init__(message)
        self.expected_statuses = expected_statuses
        self.actually_status = actually_status
        self.target_status = target_status


def get_user_by_id(uid):
    """Accept a string user id and return a account object."""
    if uid.isdigit():
        return UserAccount.query.get(int(uid))
    else:
        return UserAccount.query.filter_by(name=uid).one()


def store_user(user):
    """Store a user's account into database."""
    db.session.add(user)
    db.session.commit()


@login_manager.user_loader
def _load_user(uid):
    return get_user_by_id(uid)
