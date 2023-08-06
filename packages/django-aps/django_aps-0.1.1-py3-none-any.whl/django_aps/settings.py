"""
Apscheduler settings.
"""
from django.conf import settings
from django.core.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    'DEFAULT_DISCOVER_SCHEMA': 'database',
    'DEFAULT_DISCOVER_PKG': [
        'service',
    ],
    'DEFAULT_JOB_STORES': 'django_apscheduler.jobstores.DjangoJobStore',
    'DEFAULT_EXECUTORS': {
        'executor': 'apscheduler.executors.pool.ThreadPoolExecutor',
        'max_pool_size': 20
    },
    'DEFAULT_JOB_DEFAULTS': {
        'coalesce': False,
        'max_instances': 3
    },
    'DEFAULT_TIMEZONE': 'Asia/Shanghai'
}

IMPORT_STRINGS = [

]

REMOVED_SETTINGS = [

]


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    if isinstance(val, str):
        return import_from_string(val, setting_name)
    if isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = f"Could not import '{val}' for APS setting '{setting_name}'. {e.__class__.__name__}: {e}."
        raise ImportError(msg) from e


class APSSettings:

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self._check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'APS_SETTINGS', {})

        return self._user_settings

    def __getattr__(self, item):
        if item not in self.defaults:
            raise AttributeError(f'Invalid APS setting: "{item}"')

        try:
            val = self.user_settings[item]
        except KeyError:
            val = self.defaults[item]

        if item in self.import_strings:
            val = perform_import(val, item)

        self._cached_attrs.add(item)
        setattr(self, item, val)

        return val

    @staticmethod
    def _check_user_settings(user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(f"The '{setting}' setting has been removed. Please use available settings.")
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


aps_settings = APSSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(**kwargs):
    setting = kwargs['setting']
    if setting == 'APS_SETTINGS':
        aps_settings.reload()


setting_changed.connect(reload_api_settings)
