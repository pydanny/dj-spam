from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed

from spam.views import ReportSpamCreateView
from test_plus.test import TestCase

from test_app.models import Data


class TestReportSpamCreateView(TestCase):

    def setUp(self):
        self.data = Data.objects.create(title='test')

    def test_display_report_view(self):
        url = reverse('data', kwargs={'pk': self.data.pk})
        response = self.get(url)

        # TODO: Make this actually test for useful things
        self.assertTrue(isinstance(response, HttpResponseNotAllowed))
