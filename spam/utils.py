from django.apps import apps
from django.core.exceptions import FieldDoesNotExist


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
