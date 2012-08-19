#!/usr/bin/env python
#-*- coding:utf-8 -*-

from tests import SigmagoTestCase
from sigmago.account.models import UserAccount


class UserAccountTestCase(SigmagoTestCase):

    def test_create(self):
        """Tests creating UserAccount instance with different ways."""
        #: create without any arguments
        account_alpha = UserAccount()
        account_alpha.name = "tonyseek"
        account_alpha.email = "tonyseek@sigmago.me"
        account_alpha.nickname = "TonySeek"
        #: create with all arguments
        account_beta = UserAccount(name="tonyseek",
                                   email="tonyseek@sigmago.me",
                                   nickname="TonySeek",
                                   passwd="123456")
        #: test attributes
        self.assertEqual(account_alpha.name, "tonyseek")
        self.assertEqual(account_alpha.email, "tonyseek@sigmago.me")
        self.assertEqual(account_alpha.nickname, "TonySeek")
        self.assertEqual(account_alpha.name, account_beta.name)
        self.assertEqual(account_alpha.email, account_beta.email)
        self.assertEqual(account_alpha.nickname, account_beta.nickname)

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
