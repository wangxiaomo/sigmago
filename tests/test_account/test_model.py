#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sigmago.corelib.ext import db
from sigmago.account.models import UserAccount
from tests import SigmagoTestCase


class UserAccountTestCase(SigmagoTestCase):

    def test_create(self):
        """Tests creating UserAccount instance with different ways."""
        #: create without any arguments
        account_alpha = UserAccount()
        account_alpha.name = "tonyseek"
        account_alpha.email = "tonyseek@sigmago.me"
        account_alpha.nickname = u"TonySeek"
        #: create with all arguments
        account_beta = UserAccount(name="tonyseek",
                                   email="tonyseek@sigmago.me",
                                   nickname=u"TonySeek",
                                   passwd="123456")
        #: test attributes
        self.assertEqual(account_alpha.name, "tonyseek")
        self.assertEqual(account_alpha.email, "tonyseek@sigmago.me")
        self.assertEqual(account_alpha.nickname, "TonySeek")
        self.assertEqual(account_alpha.name, account_beta.name)
        self.assertEqual(account_alpha.email, account_beta.email)
        self.assertEqual(account_alpha.nickname, account_beta.nickname)
        #: test to store into database
        db.session.add(account_alpha)
        db.session.commit()
        db.session.delete(account_alpha)
        db.session.commit()
        db.session.add(account_beta)
        db.session.commit()
        db.session.delete(account_beta)
        db.session.commit()

    def test_password(self):
        """Tests the passwork checking feature of UserAccount."""
        #: two way to set password
        account_alpha = UserAccount()
        account_alpha.change_passwd("134565")
        account_beta = UserAccount(passwd="134565")
        #: check password to pass
        self.assertTrue(account_alpha.check_passwd("134565"))
        self.assertTrue(account_beta.check_passwd("134565"))
        #: check password to fail
        for account in [account_alpha, account_beta]:
            self.assertFalse(account.check_passwd("13456"))
            self.assertFalse(account.check_passwd("34565"))
            self.assertFalse(account.check_passwd("1345657"))
            self.assertFalse(account.check_passwd("1134565"))
            self.assertFalse(account.check_passwd("abcd"))
            self.assertFalse(account.check_passwd(""))
        #: check the effective of salt
        self.assertNotEqual(account_alpha.passwd_hash,
                            account_beta.passwd_hash)
        self.assertNotEqual(account_alpha.passwd_salt,
                            account_beta.passwd_salt)

    def test_non_case_sensitive_name(self):
        """Tests name and email of account is non case sensitive."""
        #: create model
        account = UserAccount(name="TonySeek", email="TonySeek@Gmail.COM",
                              nickname=u"TonySeek", passwd="123456")
        db.session.add(account)
        db.session.commit()
        #: compare with lower case name
        self.assertEqual(account.name, "tonyseek")
        self.assertEqual(account.email, "tonyseek@gmail.com")
        #: query
        query_by = UserAccount.query.filter_by
        self.assertIs(account, query_by(name="tonyseek").first())
        self.assertIs(account, query_by(email="tonyseek@gmail.com").first())
