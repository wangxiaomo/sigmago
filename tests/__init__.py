#!/usr/bin/env python
#-*- coding:utf-8 -*-

import inspect
import unittest

from flask.ext.testing import TestCase

from sigmago.corelib.app import make_app
from sigmago.corelib.ext import db


class TestConfig(object):
    """The test configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class SigmagoTestCase(TestCase):
    """The base class of all test cases."""

    app_count = 0
    config = TestConfig()

    def create_app(self):
        #: build app name
        import_name = inspect.getmodule(self).__name__
        app_name = "sigmago-test[%d]" % SigmagoTestCase.app_count
        SigmagoTestCase.app_count += 1
        #: create app instance
        app = make_app(import_name=import_name, app_name=app_name,
                       config=self.config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def get_oauth_remote(self, name):
        pass

    def define_models(self):
        pass


def make_test_suite():
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    return suite
