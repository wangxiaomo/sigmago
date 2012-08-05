#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.testing import TestCase

from sigmago.corelib.app import make_app


class SigmagoTestCase(TestCase):
    """The base class of all test cases."""

    def create_app(self):
        app = make_app()
        app.config["TESTING"] = True
        return app
