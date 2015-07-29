from django.db import models


class Spammable(models.Model):

    spam_flag = models.ManyToManyField("SpammyPosting")

    class Meta:
        abstract = True
