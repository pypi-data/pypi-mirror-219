#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      test_scheduler_service
   Description:
   Author:          dingyong.cui
   date：           2023/7/11
-------------------------------------------------
   Change Activity:
                    2023/7/11
-------------------------------------------------
"""
import json
import pickle
from typing import Text, Union



def setup_module():
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_aps1.settings')
    django.setup()


def test_add_job():
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.executors.pool import ThreadPoolExecutor
    from django_apscheduler.jobstores import DjangoJobStore
    from django.utils.module_loading import import_string
    from apscheduler.util import obj_to_ref, ref_to_obj
    from importlib import import_module
    options = {
        'jobstores': {
            'default': DjangoJobStore()
        },
        'executor': {
            'default': ThreadPoolExecutor(20)
        },
        'job_defaults': {
            'coalesce': True,
            'misfire_grace_time': 30,
            'max_instances': 10
        },
        'timezone': 'Asia/Shanghai'
    }
    module_path = 'django_aps.service.service_test'
    scheduler = BackgroundScheduler(**options)
    scheduler.start()
    scheduler.remove_all_jobs()
    # cls = import_string('django_aps.service.service_test.ApsTest')
    # func = cls().add1
    # func = ref_to_obj('django_aps.service.service_test:ApsTest().add1')
    # obj_to_ref(func)
    # __import__('django_aps.service.service_test', fromlist=('ApsTest',))
    # exec('from django_aps.service.service_test import ApsTest')
    # job = scheduler.add_job(func=cls.add1, kwargs={'a': 10, 'b': 3})
    job = scheduler.add_job(func='django_aps.service.service_test:ApsTest.add1', args=('self',), kwargs={'a': 10, 'b': 3})
    # job = scheduler.add_job(func=eval(f'{attr}().add1'), kwargs={'a': 10, 'b': 3})
    print(job)


def test_trigger():
    from pydantic import BaseModel
    from apscheduler.triggers.cron import CronTrigger
    params = {"year": "*", "day_of_week": "0-4", "hour": "8, 10, 17, 12, 14, 16, 18, 20, 22, 0", "minute": "0",
              "second": "0"}

    class Cron(BaseModel):
        year: Union[Text, None] = None
        month: Union[Text, None] = None
        week: Union[Text, None] = None
        day: Union[Text, None] = None
        day_of_week: Union[Text, None] = None
        hour: Union[Text, None] = None
        minute: Union[Text, None] = None
        second: Union[Text, None] = None

    ct = Cron(**params)


def test_db():
    from django_apscheduler.models import DjangoJob
    job = DjangoJob.objects.get(id='1aa0ee9543174ae8bac4e28b96260306')
    pickle.loads(job.job_state)
    print(job)
