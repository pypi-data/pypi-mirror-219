"""
Common utils
"""
from django.db import connection


def check_table_exist(name: str) -> bool:
    with connection.cursor():
        table_names = connection.introspection.table_names()
        if name in table_names:
            return True

    return False
