#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sigmago.corelib.ext import oauth
from tests import SigmagoTestCase


class OAuthExtTestCase(SigmagoTestCase):
    """Tests the oauth extension."""

    def test_builtin_app(self):
        """Tests the injected method "get_remote_app" is working."""
        google_app = oauth.get_remote_app("google")
        douban_app = oauth.get_remote_app("douban")
        assert google_app
        assert douban_app
