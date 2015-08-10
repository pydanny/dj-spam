#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-spam
------------

Tests for `dj-spam` utils module.
"""
from base64 import b16encode

from django.contrib.auth import get_user_model
from django.test import TestCase

from spam.exceptions import B16DecodingFail
from spam.utils import (
    get_app_name,
    b16_slug_to_arguments
)

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


class TestB16SlugToArguments(TestCase):

    def setUp(self):
        self.slug = b16encode('myapp/myproject/35'.encode('utf-8'))
        self.bad_slug = 'ABCDEF'.encode('utf-8')
        self.bad_slug_type = 'IAMSPAM'

    def test_b16_slug_to_arguments(self):
        self.assertEqual(
            ('myapp', 'myproject', '35'),
            b16_slug_to_arguments(self.slug)
        )

    def test_bad_slug(self):
        with self.assertRaises(B16DecodingFail):
            b16_slug_to_arguments(self.bad_slug)

    def test_bad_slug_type(self):
        with self.assertRaises(B16DecodingFail):
            b16_slug_to_arguments(self.bad_slug_type)
