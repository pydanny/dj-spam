# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spammyposting',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spammyposting',
            name='reviewer',
            field=models.ForeignKey(related_name='reviewer', blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='spammyposting',
            name='status',
            field=models.IntegerField(default=10, choices=[(10, 'Flagged'), (20, 'Under review'), (30, 'Rejected'), (40, 'Approved')]),
        ),
        migrations.AlterField(
            model_name='spammyposting',
            name='reporter',
            field=models.ForeignKey(related_name='reporter', blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
