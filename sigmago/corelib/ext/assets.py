#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path

from flask.ext.assets import Bundle


public_scripts = (
    "http://code.jquery.com/jquery-1.8.1.js",
    "https://raw.github.com/twitter/bootstrap/master/js/bootstrap-alert.js",
    "https://raw.github.com/twitter/bootstrap/master/js/bootstrap-button.js",
)

debug_public_scripts = (
    "http://lesscss.googlecode.com/files/less-1.3.0.js",
)

public_less_stylesheets = (
    "https://raw.github.com/twitter/bootstrap/master/less/bootstrap.less",
)


def make_public_scripts_bundle(output, is_debug=False):
    scripts = public_scripts[:]
    if is_debug:
        scripts.extend(debug_public_scripts)
    return Bundle(*scripts, filters="rjsmin", output=output)


def make_less_stylesheets_bundle(stylesheets, output, is_debug=False):
    extra = {}
    if is_debug:
        extra['rel'] = "stylesheet/less"
    else:
        extra['rel'] = "stylesheet"
    return Bundle(*stylesheets, filters="less", output=output, extra=extra)


def setup_app_assets(assets, root_path):
    """Set up all application level assets."""
    assets.from_yaml(os.path.join(root_path, "config/assets.yaml"))
