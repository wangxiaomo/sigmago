#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import current_app


OAUTH_REMOTE_NAMES = ["google", "douban"]


def setup_oauth_remotes(oauth_ext, config, namespace):
    """Setups all remotes with the given factory.

    The configuration such as app_key and app_secret should be assigned in
    the argument 'config'.

    Example: config = {'OAUTH_GOOGLE_APP_ID': "abcdefg"}
    """
    for remote_name in OAUTH_REMOTE_NAMES:
        #: build a new name with namespace
        if namespace:
            remote_name_ns = "%s:%s" % (namespace, remote_name)
        else:
            remote_name_ns = remote_name
        #: get app_id and app_secret id from app config files
        prefix = "OAUTH_%s_" % remote_name.upper()
        app_id = config[prefix + "APP_ID"]
        app_secret = config[prefix + "APP_SECRET"]
        #: setup the remote application
        make_remote = globals()['make_%s_remote' % remote_name]
        make_remote(oauth_ext, app_id, app_secret, remote_name_ns)


def get_remote_app(oauth_ext, name):
    """Gets a oauth remote application client in current request context."""
    namespace = getattr(current_app, "app_name", None)  # app_name is namespace
    name_ns = name if not namespace else "%s:%s" % (namespace, name)
    return oauth_ext.remote_apps[name_ns]


def make_google_remote(oauth_ext, app_id, app_secret, name="google"):
    """Creates the oauth remote of Google API."""
    base_url = "https://www.google.com/accounts/"
    authorize_url = "https://accounts.google.com/o/oauth2/auth"
    url_prefix = "https://www.googleapis.com/"
    request_params = {'scope': url_prefix + "auth/userinfo.email",
                      'response_type': "code"}
    access_token_url = "https://accounts.google.com/o/oauth2/token"
    access_params = {'grant_type': "authorization_code"}

    ext = oauth_ext.remote_app(name, base_url=base_url,
                               authorize_url=authorize_url,
                               request_token_url=None,
                               request_token_params=request_params,
                               access_token_url=access_token_url,
                               access_token_method="POST",
                               access_token_params=access_params,
                               consumer_key=app_id,
                               consumer_secret=app_secret)
    return ext


def make_douban_remote(oauth_ext, app_id, app_secret, name="douban"):
    """Creates the oauth remote of Douban API."""
    base_url = "http://api.douban.com/"
    authorize_url = "https://www.douban.com/service/auth2/auth"
    request_params = {'response_type': "code"}
    access_token_url = "https://www.douban.com/service/auth2/token"
    access_params = {'grant_type': "authorization_code"}

    ext = oauth_ext.remote_app(name, base_url=base_url,
                               authorize_url=authorize_url,
                               request_token_url=None,
                               request_token_params=request_params,
                               access_token_url=access_token_url,
                               access_token_method="POST",
                               access_token_params=access_params,
                               consumer_key=app_id,
                               consumer_secret=app_secret)
    return ext
