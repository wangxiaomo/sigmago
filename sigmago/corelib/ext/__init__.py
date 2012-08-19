#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.assets import Environment
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from flask.ext.oauth import OAuth
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy

from sigmago.corelib.ext.oauth import setup_oauth_remotes


OAUTH_REMOTE_NAMES = ("google", "douban")

assets = Environment()
babel = Babel()
login_manager = LoginManager()
oauth = OAuth()
openid = OpenID()
db = SQLAlchemy()


def setup_extensions_with_app(app):
    """Setups all extension to the given app."""
    assets.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    setup_oauth_remotes(oauth, app.config,
                        namespace=getattr(app, "app_name", None))
    openid.init_app(app)
