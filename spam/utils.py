from __future__ import unicode_literals

from binascii import Error as BinaryError
from base64 import b16encode, b16decode

from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404

from .exceptions import B16DecodingFail


def spammables():
    # Lists all models that are marked flaggable
    flaggables = []
    for model in apps.get_models():
        try:
            model._meta.get_field_by_name('spam_flag')
        except FieldDoesNotExist:
            continue
        flaggables.append(model)
    return flaggables


def is_spammable(app, model):
    model_class = apps.get_model("{}.{}".format(app, model))
    return model_class in spammables()


def get_app_name(model_class_or_instance):
    return model_class_or_instance._meta.app_config.name.split('.')[-1]


def b16_slug_to_arguments(b16_slug):
    """

        Raises B16DecodingFail exception on
    """
    try:
        url = b16decode(b16_slug.decode('utf-8'))
    except BinaryError:
        raise B16DecodingFail
    except TypeError:
        raise B16DecodingFail('Non-base16 digit found')
    except AttributeError:
        raise B16DecodingFail("b16_slug must have a 'decode' method.")

    try:
        app, model, pk = url.decode('utf-8').split('/')[0:3]
    except UnicodeDecodeError:
        raise B16DecodingFail("Invalid b16_slug passed")
    return app, model, pk


def get_spammable_or_404(app, model, pk):
    # Does this view have the is_spammable mixin?
    if is_spammable(app, model):
        # convert app/model into the actual model class
        model_class = apps.get_model(app, model)
        # So we can call meta for details in the template
        model_class.meta = model_class._meta
        instance = get_object_or_404(model_class, pk=pk)
        return model_class, instance
    raise Http404
