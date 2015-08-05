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
        url = reverse('data', kwargs={'pk': self.data.pk})
        # Create a request
        request = self.factory.get(url)
        # Generate a response
        view = DataDetailView.as_view()(request)
        response = view(request)

        # Check to see if we had a 404 or not
        self.response_200(response)

    def test_slug_to_arguments(self):
        base_url = "test_app/data/15/"
        b16_slug = b16encode(base_url.encode('utf-8'))
        url = reverse('spam:report', kwargs={'slug': b16_slug})


        request = self.factory.get(url)
        import ipdb; ipdb.set_trace()

        view = ReportSpamCreateView.as_view()
        response = view(request)
