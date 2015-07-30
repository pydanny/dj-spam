from django.contrib import admin
from django.utils.safestring import mark_safe

from .behaviors import Spammable
from .exceptions import SpamNotFound
from .models import SpammyPosting
from .utils import spammables

class SpammyPostingAdmin(admin.ModelAdmin):
    model = SpammyPosting
    readonly_fields = ('source', 'created', 'modified',)

    def source(self, instance):
        """This links directly to the location of the offending content."""

        for spammable in spammables():
            try:
                content = spammable.objects.get(spam_flag=instance.pk)
            except SpammyPosting.DoesNotExist:
                continue
            break
        else:
            raise SpamNotFound(spammable)

        response = """<a href="{0}">{1}</a>""".format(
                content.get_absolute_url(),
                content
            )

        return mark_safe(response)

    source.short_description = "Source URL"
    source.allow_tags = True

admin.site.register(SpammyPosting, SpammyPostingAdmin)
