#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-spam
------------

Tests for `dj-spam` models module.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from spam.utils import get_app_name

User = get_user_model()


class TestGetAppName(TestCase):
    """ Tests the `get_app_name()` utility. """

    def test_model_class(self):
        """ Tests `get_app_name()` with a model class as the argument. """
        app_name = get_app_name(User)
        self.assertEqual(
            app_name,
            'auth'  # django.contrib.auth
        )

    def test_instance(self):
        """ Tests `get_app_name()` with a model instance as the argument. """
        user = User.objects.create(
            username='test',
            email='test@example.com',
            password='!'
        )
        app_name = get_app_name(user)
        self.assertEqual(
            app_name,
            'auth'  # django.contrib.auth
        )
