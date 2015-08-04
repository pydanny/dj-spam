from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed
from django.test import RequestFactory

from spam.views import ReportSpamCreateView
from test_plus.test import TestCase

from test_app.models import Data
from test_app.views import DataDetailView


class TestReportSpamCreateView(TestCase):

    def setUp(self):
        self.data = Data.objects.create(title='test')
        self.factory = RequestFactory()

    def test_data_detail_view(self):
        """ Just to make certain we have the tests wired up right"""
        # Get the URL
        url = reverse('data', kwargs={'pk': self.data.pk})
        # Create a request
        request = self.factory.get(url)
        # Generate a response
        response = DataDetailView.as_view()(request)

        # Check to see if we had a 404 or not
        self.response_200(response)
