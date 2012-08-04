#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path

from flask import Flask

from sigmago.corelib.ext import setup_extensions_with_app


CONFIG_BUILTIN = "sigmago.config.app"
CONFIG_ENV_NAME = "SIGMAGO_CONFIG"


def make_app(config=None):
    """Creates an application instance."""
    #: creates app instance
    app = Flask(__name__)
    #: loads built-in configuration
    app.config.from_object(CONFIG_BUILTIN)
    #: loads outside configuration
    if not config:
        app.config.from_envvar(CONFIG_ENV_NAME)
    elif os.path.exists(config):
        app.config.from_pyfile(config)
    else:
        app.config.from_object(CONFIG_ENV_NAME)
    #: setups extensions
    setup_extensions_with_app(app)
    return app
