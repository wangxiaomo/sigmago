#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import request, flash, render_template, url_for, redirect, abort
from flask.views import View
from flask.ext.babel import lazy_gettext as _

from sigmago.corelib.ext import db
from sigmago.account import app
from sigmago.account.views import forms
from sigmago.account.models import UserAccount, UserStatusError


@app.errorhandler(UserStatusError)
def handle_user_status_error(error):
    #: TODO give it a html page
    return str(error), 403


class SignUpView(View):
    """The view of signing up flow."""

    UI_TEMPLATE = "signup.html"

    def dispatch_request(self):
        #: after the process completed, return this page
        #: TODO use "url_for" there to point home page
        self.next_url = request.args.get("next", "/")

        #: confirm token to activate account
        activate_token = request.args.get("token", None)
        #: user's name to give a confirm prompt
        name = request.args.get("name", None)

        #: creates the form validator
        self.form = forms.SignUpForm()

        if request.method == "GET":
            if name:
                #: fetch model
                self.account = UserAccount.query.get_by_uid(name) or abort(404)

                if self.account.status == "unactivated":
                    if activate_token:
                        #: both name and token were provided,
                        #: try to activate the account
                        return self.activate(activate_token)
                    else:
                        #: the account has not been activated,
                        #: but there is not token provided,
                        #: then give a confirm prompt.
                        return self.finished_signup()
                else:
                    #: the account has been activated
                    return self.finished_activate()
            else:
                #: there is not user's id/name provided, then shows the form
                return self.show()

        if request.method == "POST" and self.form.validate():
            #: fills in account information
            return self.signup()

        #: show error messages
        return self.show()

    def show(self):
        """Shows the UI."""
        return render_template(self.UI_TEMPLATE, **vars(self))

    def signup(self):
        """Fills in account information and sends confirm email."""
        #: creates a model from the filled form
        self.account = UserAccount(name=self.form.name.data,
                                   email=self.form.email.data,
                                   nickname=self.form.nickname.data)
        self.account.change_passwd(self.form.passwd.data)
        #: store into database
        db.session.add(self.account)
        db.session.commit()
        #: flash a prompt message
        flash(_("The email to confirm your joined has been send."), "infor")
        #: redirect to next page
        return redirect(url_for("account.signup", name=self.account.name))

    def activate(self, token):
        """Activates the account by provided token."""
        pass

    def finished_signup(self):
        #: TODO give a prompt "The email has been send"
        return repr(vars(self.account))

    def finished_activate(self):
        #: TODO give a prompt "The sign up process has been finished success."
        return repr(vars(self.account))


app.add_url_rule("/signup",
                 view_func=SignUpView.as_view("signup"),
                 methods=["GET", "POST"])
