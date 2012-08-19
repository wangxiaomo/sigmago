#!/usr/bin/env python
#-*- coding:utf-8 -*-

import inspect

from flask.ext.testing import TestCase

from sigmago.corelib.app import make_app


class SigmagoTestCase(TestCase):
    """The base class of all test cases."""

    def create_app(self):
        #: create app instance
        import_name = inspect.getmodule(self).__name__
        app = make_app(import_name)
        app.config["TESTING"] = True
        return app
