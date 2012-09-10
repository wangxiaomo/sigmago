#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path

from jinja2 import nodes
from jinja2.ext import Extension
from webassets.env import RegisterError


class ContextAssetsExtension(Extension):
    """A extension to support extending context assets by names in template.

    Those names are defined by bundles of Flask-Assets extension.

    Usage Example:

        {% extends "layout.html" %}
        {% scripts "scripts.photo-album", "scripts.dialog" %}
        {% stylesheets "stylesheets.dialog" %}

    The names will be appended to context variable "assets_stylesheets" and
    "assets_scripts".
    """

    tags = {'stylesheets': "assets_stylesheets",
            'scripts': "assets_scripts"}

    def parse(self, parser):
        token = next(parser.stream)
        #: assets names
        assets_names = parser.parse_tuple()
        #: get bundle variable
        bundle_name = self.tags[token.value]
        bundle = nodes.Getattr(nodes.ContextReference(), bundle_name, "load")
        #: calling method
        extend_bundle = nodes.Getattr(bundle, "extend", "load")
        call = nodes.Call(extend_bundle, [assets_names], [], None, None)
        #: execute inline
        expr = nodes.ExprStmt(lineno=token.lineno)
        expr.node = call
        return expr


def setup_app_assets(app, assets):
    """Set up all application level assets."""
    app.jinja_env.add_extension(ContextAssetsExtension)

    try:
        assets.from_yaml(os.path.join(app.root_path, "config/assets.yaml"))
    except RegisterError as error:
        #: ignore repeat loading in testing
        if not app.config['TESTING']:
            raise error

    @app.context_processor
    def assets_names():
        scripts = ["scripts.public"]
        stylesheets = ["stylesheets.public"]
        return {'assets_scripts': scripts, 'assets_stylesheets': stylesheets,
                'extend_scripts': scripts.extend, }
