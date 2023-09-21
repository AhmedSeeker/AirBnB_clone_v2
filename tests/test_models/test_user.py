#!/usr/bin/python3
""" """
from models.user import User
import unittest


class test_User(unittest.TestCase):
    """ """

    def setUp(self):
        """First call"""
        self.user = User("aa", "bb", "cc", "dd")

    def test_first_name(self):
        """ """
        self.user = User()
        self.assertEqual(self.user.first_name, "")

    def test_last_name(self):
        """ """
        self.assertEqual(type(self.user.last_name), str)

    def test_email(self):
        """ """
        self.assertEqual(type(self.user.email), str)

    def test_password(self):
        """ """
        self.assertEqual(type(user.password), str)
