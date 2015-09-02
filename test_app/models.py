from django.core.urlresolvers import reverse_lazy
from django.db import models

from spam import Spammable


class Data(Spammable, models.Model):

    title = models.CharField(max_length=50)

    def get_absolute_url(self):
        # Not required, but it allows dj-spam to link back to the offending
        # content in the report spam view.
        return reverse_lazy('data', kwargs={'pk': self.pk})
