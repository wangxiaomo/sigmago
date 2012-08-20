#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.blueprints import Blueprint


__all__ = ("models", "views")

app = Blueprint("account", __name__, template_folder="templates",
                static_folder="static", url_prefix="")
