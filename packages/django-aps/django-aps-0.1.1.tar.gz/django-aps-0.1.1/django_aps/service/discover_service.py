"""
Discover service
"""
import logging
from typing import List, Dict

from django.db import transaction

from django_aps.repository import apscheduler_func_model_mapper
from django_aps.settings import aps_settings
from django_aps.utils.common import check_table_exist
from django_aps.utils.discover import autodiscover_aps

logger = logging.getLogger(__name__)


class DiscoverService:

    def __init__(self, schema: str = None):
        self._schema = schema

    @property
    def schema(self):
        if self._schema is None:
            self._schema = aps_settings.DEFAULT_DISCOVER_SCHEMA

        return self._schema

    def get_apscheduler_funcs(self, name: str = None):
        if self.schema == 'database':
            return apscheduler_func_model_mapper.get_aps_funcs(name)

        return self.discover_apscheduler(name)

    @staticmethod
    def discover_apscheduler(name: str = None) -> List[Dict]:
        """ Discover apscheduler functions

        :param str name: which function name contain it
        """
        aps_funcs = autodiscover_aps()
        if name is None:
            return aps_funcs
        aps_name_funcs = []
        for aps_func in aps_funcs:
            if name in aps_func.get('func_name'):
                aps_name_funcs.append(aps_func)

        return aps_name_funcs

    def sync_aps_to_db(self):
        """
        Synchronize auto discover django_aps function to the database

        """
        if self.schema != 'database':
            logger.warning(f'Skip sync because current schema is {self.schema} not equal database.')
            return
        if not check_table_exist('django_apscheduler_func'):
            logger.warning('Skip sync because table "django_apscheduler_func" does not exist.')
            return
        logger.info('Start sync apscheduler func to database.')
        aps_funcs = autodiscover_aps()
        with transaction.atomic():
            apscheduler_func_model_mapper.delete_aps_funcs(is_all=True)
            apscheduler_func_model_mapper.save_aps_funcs(aps_funcs)
        logger.info('apscheduler func has been synchronized.')
