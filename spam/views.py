from django.apps import apps
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    TemplateView,
)

from .models import SpammyPosting
from .utils import (
    spammables,
    is_spammable,
    get_app_name
)


class ReportSpamCreateView(CreateView):
    """
    Requires 'model' as an argument
    """
    model = SpammyPosting
    fields = ['comment',]
    success_url = reverse_lazy('spam:thanks')

    def get_spammable_or_404(self, app, model, pk):
        # Does this have the is_spammable mixin?
        if is_spammable(app, model):
            # convert app/model into the actual model class
            model_class = apps.get_model(app, model)
            # So we can call meta for details in the template
            model_class.meta = model_class._meta
            instance = get_object_or_404(model_class, pk=pk)
            return model_class, instance
        raise Http404


    def get_context_data(self, **kwargs):
        context = super(ReportSpamCreateView, self).get_context_data(**kwargs)
        app, model, pk = self.kwargs['app'], self.kwargs['model'], self.kwargs['pk']
        model_class, instance = self.get_spammable_or_404(app, model, pk)
        context['model_class'] = model_class
        context['instance'] = instance
        return context

    def form_valid(self, form):
        spam = form.save(commit=False)
        spam.reporter = self.request.user
        spam.save()
        self.app, model, pk = self.kwargs['app'], self.kwargs['model'], self.kwargs['pk']
        return super(ReportSpamCreateView, self).form_valid(form)


class ThankYouView(TemplateView):
    template_name = "spam/thanks.html"


class SpammableMixin(object):
    def spam_report_url(self):
        return reverse('spam:report', kwargs={
            'app': get_app_name(self.object),
            'model': self.object._meta.object_name,
            'pk': self.object.pk
        })
