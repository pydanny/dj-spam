from binascii import Error as BinaryError
from base64 import b16encode

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

from .exceptions import B16DecodingFail
from .models import SpammyPosting
from .utils import (
    spammables,
    is_spammable,
    get_app_name,
    b16_slug_to_arguments,
    get_spammable_or_404
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

    def b16_slug_to_arguments(self):
        """Returns app, model, pk"""
        try:
            return b16_slug_to_arguments(self.kwargs['slug'])
        except B16DecodingFail:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ReportSpamCreateView, self).get_context_data(**kwargs)
        app, model, pk = self.b16_slug_to_arguments()
        model_class, instance = get_spammable_or_404(app, model, pk)
        context['model_class'] = model_class
        context['instance'] = instance
        return context

    def form_valid(self, form):
        app, model, pk = self.b16_slug_to_arguments()
        model_class, instance = get_spammable_or_404(app, model, pk)
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
        slug = "{app}/{model}/{pk}/".format(
            app = get_app_name(self.object),
            model = self.object._meta.object_name,
            pk = self.object.title
        )
        # We're just hashing so users won't readily get a sense of how we
        # architected our project
        b16_slug = b16encode(slug.encode('utf-8'))
        return reverse_lazy('spam:report', kwargs={'b16_slug': b16_slug})
