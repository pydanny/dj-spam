from base64 import b16encode, b16decode

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
        # Create a request
        request = self.factory.get('/fake-url')
        # Generate a response
        response = DataDetailView.as_view()(request, pk=self.data.pk)

        # Check to see if we had a 404 or not
        self.response_200(response)

    def test_slug_to_arguments(self):
        base_url = "test_app/data/{0}/".format(self.data.pk)
        b16_slug = b16encode(base_url.encode('utf-8'))

        request = self.factory.get('/fake-url')

        view = ReportSpamCreateView.as_view()
        response = view(request, slug=b16_slug)
        self.response_200(response)
