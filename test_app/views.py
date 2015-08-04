from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from spam import SpammableMixin

from .models import Data


class DataDetailView(SpammableMixin, View):

    @property
    def object(self):
        return get_object_or_404(Data, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return HttpResponse()
