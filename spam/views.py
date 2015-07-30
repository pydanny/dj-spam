from django.apps import apps
from django.conf import settings
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db import transaction
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

# MANAGERS is a list of tuples following the same pattern as settings.ADMINS
MANAGERS = getattr(settings, "MANAGERS", settings.ADMINS)


class ReportSpamCreateView(CreateView):
    """
    Requires 'model' as an argument
    """
    model = SpammyPosting
    fields = ['comment',]
    success_url = reverse_lazy('spam:thanks')

    def get_spammable_or_404(self, app=None, model=None, pk=None):
        if app is None and model is None and pk is None:
            app, model, pk = self.kwargs['app'], self.kwargs['model'], self.kwargs['pk']
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
        model_class, instance = self.get_spammable_or_404()
        context['model_class'] = model_class
        context['instance'] = instance
        return context

    def form_valid(self, form):
        model_class, instance = self.get_spammable_or_404()
        with transaction.atomic():
            spam = form.save(commit=False)
            spam.reporter = self.request.user
            spam.save()
            # Add the spam to the flagged instance of content
            instance.spam_flag.add(spam)
        mail_managers(
            # TODO: Ability to specify site name
            "Spam flagged on your site",
            # TODO: Put this in a template so it can be easily customized
            "Content was flagged as being spammy. You should go and check it out."
        )
        return super(ReportSpamCreateView, self).form_valid(form)


class ThankYouView(TemplateView):
    template_name = "spam/thanks.html"


class SpammableMixin(object):
    def spam_report_url(self):
        return reverse_lazy('spam:report', kwargs={
            'app': get_app_name(self.object),
            'model': self.object._meta.object_name,
            'pk': self.object.pk
        })
