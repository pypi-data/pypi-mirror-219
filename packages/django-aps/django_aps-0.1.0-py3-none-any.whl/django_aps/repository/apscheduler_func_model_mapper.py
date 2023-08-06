"""
APScheduler func model mapper
"""
from typing import Union, List, Dict

from django_aps.models import ApschedulerFunc


def get_aps_funcs(name: str = None, **kwargs) -> Union[List, None]:
    if name:
        kwargs.setdefault('func_name__contains', name)
    aps_funcs_queryset = ApschedulerFunc.objects.filter(
        **kwargs
    )
    if aps_funcs_queryset.exists():
        return list(aps_funcs_queryset.values())

    return None


def save_aps_funcs(aps_funcs: List[Dict]):
    objs = []
    for aps_func in aps_funcs:
        objs.append(ApschedulerFunc(**aps_func))
    ApschedulerFunc.objects.bulk_create(
        objs
    )


def delete_aps_funcs(conditions: Dict = None, is_all: bool = False):
    if is_all:
        queryset = ApschedulerFunc.objects.all()
    else:
        queryset = ApschedulerFunc.objects.filter(
            **conditions
        )
    deleted, _rows_count = queryset.delete()

    return deleted
