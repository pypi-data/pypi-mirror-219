#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      test_discover
   Description:
   Author:          dingyong.cui
   date：           2023/7/7
-------------------------------------------------
   Change Activity:
                    2023/7/7
-------------------------------------------------
"""


def setup_module():
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_aps1.settings')
    django.setup()


def test_autodiscover_aps():
    from django_aps.utils.discover import autodiscover_aps
    aps = autodiscover_aps()
    print(aps)


def test_cache():
    from django.core.cache import cache
    import time
    cache.set('test', 'balabala', 600)
    print('1 ->', cache.ttl('test'))
    time.sleep(2)
    print('2 ->', cache.ttl('test'))
