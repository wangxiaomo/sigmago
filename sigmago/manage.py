#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.script import Manager, prompt_bool

from sigmago.corelib.app import make_app
from sigmago.corelib.ext import db


app = make_app("sigmago.manage")
manager = Manager(app)


@manager.command
def create_db():
    """Creates table schema of database."""
    db.create_all()


@manager.command
def drop_db():
    """Drops all tables of database."""
    if prompt_bool("Confirm to drop all table from database"):
        db.drop_all()
