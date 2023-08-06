"""
Auto discover apscheduler
"""
import importlib
import inspect
import logging
import os.path
import pkgutil
from typing import List

from django.apps import apps

from django_aps.settings import aps_settings
from django_aps.utils.register import Register

logger = logging.getLogger(__name__)


def autodiscover_aps(custom_pkgs: List[str] = None) -> List:
    aps_funcs = []
    discover_pkgs = aps_settings.DEFAULT_DISCOVER_PKG
    if custom_pkgs:
        discover_pkgs.extend(custom_pkgs)
    if discover_pkgs is None:
        logger.warning('Skip to discover because there is no package.')
        return aps_funcs

    for pkg in discover_pkgs:
        aps_funcs.extend(discover_pkg(pkg))

    return aps_funcs


def discover_pkg(pkg: str):
    pkg_aps_funcs = []
    for app_config in apps.get_app_configs():
        module = app_config.module
        # pkg_path = f'{pkg.__path__[0]}\\{relate_name}'
        pkg_path = os.path.join(module.__path__[0], pkg)
        pkg_name = f'{module.__name__}.{pkg}'
        part_aps_funcs = _autodiscover_aps(pkg_path, pkg_name)
        pkg_aps_funcs.extend(part_aps_funcs)

    return pkg_aps_funcs


def _autodiscover_aps(pkg_path, pkg_name):
    part_aps_funcs = []
    for _, file, _ in pkgutil.iter_modules([pkg_path]):
        py_module = importlib.import_module(f'.{file}', package=pkg_name)
        for _, p_cls in inspect.getmembers(py_module):
            if isinstance(p_cls, Register):
                for func in p_cls.items():
                    aps_func = _convert_func(func)
                    part_aps_funcs.append(aps_func)

    return part_aps_funcs


def _convert_func(func: tuple):
    func = func[1]
    func_module = func.__module__
    func_name = func.__qualname__
    func_doc = func.__doc__

    func_args = inspect.getfullargspec(func).args

    aps_func = {
        'func_module': func_module,
        'func_name': func_name,
        'func_args': func_args,
        'func_doc': func_doc
    }

    return aps_func
