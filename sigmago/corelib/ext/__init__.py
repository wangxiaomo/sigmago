#!/usr/bin/env python
#-*- coding:utf-8 -*-

import functools

from flask.ext.assets import Environment
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from flask.ext.oauth import OAuth
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.superadmin import Admin

from sigmago.corelib.ext.oauth import setup_oauth_remotes, get_remote_app


OAUTH_REMOTE_NAMES = ("google", "douban")

assets = Environment()
babel = Babel()
login_manager = LoginManager()
oauth = OAuth()
openid = OpenID()
db = SQLAlchemy()
admin = Admin()

#: wraps the "get_remote_app" function to an instance method
oauth.get_remote_app = functools.partial(get_remote_app, oauth)


def setup_extensions_with_app(app):
    """Setups all extension to the given app."""
    assets.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    setup_oauth_remotes(oauth, app.config,
                        namespace=getattr(app, "app_name", None))
    openid.init_app(app)
    admin.init_app(app)
    db.init_app(app)


def admin_managed(model_class):
    """A decorator to register a model class to super admin."""
    admin.register(model_class, session=db.session)
    return model_class
