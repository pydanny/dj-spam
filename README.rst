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

Quickstart
----------

Install dj-spam::

    pip install dj-spam

For any model you want to flag::

    from spam.models import Spammable

    class MyModel(Spammable, models.Model):
        # Define your model here. Spammable attaches
        #   the spam_flag field to your model as a ManyToManyField.


Features
--------

* Direct foreign key from the model to the spam report. Avoiding content types and using explicit foreign keys makes for less kludgy databases.
* Powered by conventions used all over Django:

  * Have the appropriate ``__str__`` or ``__unicode`` method on your models.
  * Flaggable models should have ``get_absolute_url`` methods.
