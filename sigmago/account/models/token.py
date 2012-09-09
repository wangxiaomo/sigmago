#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sigmago.corelib.ext import db, admin_managed


@admin_managed
class UserToken(db.Model):
    """The tokens of accounts."""

    id = db.Column(db.Integer, primary_key=True)
