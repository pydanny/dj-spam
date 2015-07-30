# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SpammyPosting(models.Model):

    FLAGGED = 10
    REVIEW = 20
    CONTENT_REJECTED = 30
    CONTENT_APPROVED = 40
    STATUS = (
        (FLAGGED, _('Flagged')),
        (REVIEW, _('Under review')),
        (CONTENT_REJECTED, _('Rejected')),
        (CONTENT_APPROVED, _('Approved')),
    )

    # Reporter, left null/blank in case anonymous users are allowed to submit
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='reporter')
    status = models.IntegerField(choices=STATUS, default=FLAGGED)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='reviewer')
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'spam'

    def __str__(self):
        return self.get_status_display()
