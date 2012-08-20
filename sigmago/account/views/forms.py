#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.wtf import TextField, PasswordField, SubmitField
from flask.ext.wtf import email, required, length, equal_to
from flask.ext.babel import lazy_gettext as _

from sigmago.corelib.ext.forms import Form


class SignUpForm(Form):
    """The form of signing up."""

    name = TextField(_("Account ID"), [required(), length(1, 15)])
    email = TextField(_("Email Address"), [required(), email()])
    nickname = TextField(_("Nick Name"), [length(0, 30)])
    passwd = PasswordField(_("Password"), [required(), length(6, 36)])
    confirm_passwd = PasswordField(_("Confirm Password"), [
        equal_to("passwd", message=_("Password do not match."))
    ])
    submit = SubmitField(_("Sign Up"))
