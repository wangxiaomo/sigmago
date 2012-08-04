#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.script import Manager

from sigmago.corelib.app import make_app
from sigmago.corelib.ext import db


app = make_app()
manager = Manager(app)


@manager.command
def create_db():
    """Creates table schema of database."""
    db.create_all()
