#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path

from werkzeug import import_string
from flask import Flask

from sigmago.corelib.ext import setup_extensions_with_app


CONFIG_BUILTIN = "sigmago.config.app"
CONFIG_ENV_NAME = "SIGMAGO_CONFIG"


def make_app(import_name=None, config=None, app_name="sigmago"):
    """Creates an application instance."""
    #: creates app instance
    app = Flask(import_name or __name__)
    app.app_name = app_name
    #: loads built-in configuration
    app.config.from_object(CONFIG_BUILTIN)
    #: loads outside configuration
    if not config:
        app.config.from_envvar(CONFIG_ENV_NAME)
    elif os.path.exists(config):
        app.config.from_pyfile(config)
    else:
        app.config.from_object(config)
    #: setups extensions
    setup_extensions_with_app(app)
    #: mount blueprints
    app.config.setdefault("BUILTIN_BLUEPRINTS", [])
    for blueprint_name in app.config['BUILTIN_BLUEPRINTS']:
        mount_blueprint(app, blueprint_name)
    #: return the initialized application instance
    return app


def mount_blueprint(app, name):
    """Mounts a blueprint and its package members on an application."""
    #: import blueprint and its bound package
    blueprint = import_string(name)
    package = import_string(blueprint.import_name)
    #: import the package members
    for member_name in getattr(package, "__all__", []):
        import_string("%s.%s" % (blueprint.import_name, member_name))
    #: mount the blueprint
    app.register_blueprint(blueprint)
