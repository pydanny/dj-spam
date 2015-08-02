#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-spam
------------

Tests for `dj-spam` models module.
"""

import os
import shutil
from test_plus.test import TestCase

from django.conf import settings

from spam.models import SpammyPosting


class TestSpammyPosting(TestCase):
    """ Tests for SpammyPosting model. """

    def setUp(self):
        self.user = self.make_user()
        self.spammy_posting = SpammyPosting.objects.create(
            reporter=self.user,
            status=SpammyPosting.FLAGGED,
            reviewer=self.user,
            comment="Includes too many links"
        )

    def test_str(self):
        """ Test the `__str__()` method of SpammyPosting  """
        self.assertEqual(self.spammy_posting.__str__(), "Flagged")
