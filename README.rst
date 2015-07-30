=============================
Work in Progress: dj-spam
=============================

.. image:: https://badge.fury.io/py/dj-spam.png
    :target: https://badge.fury.io/py/dj-spam

.. image:: https://travis-ci.org/pydanny/dj-spam.png?branch=master
    :target: https://travis-ci.org/pydanny/dj-spam

Django + Flagging Spam Made Easy

Documentation
-------------

The full documentation is at https://dj-spam.readthedocs.org.

Features
--------

* For Django 1.8+
* For Python 2.7/3.3+
* Direct foreign key from the model to the spam report. Avoiding content types and using explicit foreign keys makes for less kludgy databases.
* Powered by conventions used all over Django:

  * Have the appropriate ``__str__()`` or ``__unicode__()`` method on your models.
  * Flaggable models should have ``get_absolute_url()`` methods.


Quickstart
----------

Install dj-spam::

    pip install dj-spam

Configure it into your project::

    # settings.py
    INSTALLED_APPS += ['spam', ]

::

    # urls.py
    url(r'^spam/', include('spam.urls', namespace='spam')),

For any model you want to flag::

    from spam import Spammable

    class MyModel(Spammable, models.Model):
        # Define your model here. Spammable attaches
        #   the spam_flag field to your model as a ManyToManyField.

        @models.permalink
        def get_absolute_url(self):
            # Not required, but it allows dj-spam to link back to the offending
            # content in the report spam view.
            return 'absolute link to model detail view'

Run Migrations

::

    ./manage migrate

Then, in the model's related view::

    from spam import SpammableMixin

    class MyModelDetailView(SpammableMixin, DetailView):
        class = MyModel

This empowers you with the view method ``spam_report_url`` which you can use to
define the URL to the reporting form::

    <a href="{{ view.spam_report_url }}">Report Spam</a>

admin
------

dj-spam comes with a simple admin view.

emailing managers
-------------------

dj-spam emails `settings.MANAGERS` every time something is flagged. If you don't
set `settings.MANAGERS`, it will email `settings.ADMINS`.
