#!/usr/bin/env python
#-*- coding:utf-8 -*-

import inspect
import unittest

from flask.ext.testing import TestCase

from sigmago.corelib.app import make_app


class SigmagoTestCase(TestCase):
    """The base class of all test cases."""

    app_count = 0

    def create_app(self):
        #: build app name
        import_name = inspect.getmodule(self).__name__
        app_name = "sigmago-test-%d" % id(self.__class__.app_count)
        self.__class__.app_count += 1
        #: create app instance
        app = make_app(import_name=import_name, app_name=app_name)
        app.config["TESTING"] = True
        return app

    def get_oauth_remote(self, name):
        pass


def make_test_suite():
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    return suite
