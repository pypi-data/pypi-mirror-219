"""
Trigger models
"""
from __future__ import annotations

from enum import Enum
from typing import Union, Text

from pydantic import BaseModel


class TriggerType(Enum):
    CRON = 'cron'
    INTERVAL = 'interval'
    DATE = 'date'


class CronTriggerModel(BaseModel):
    year: Union[Text, None] = "*"
    month: Union[Text, None] = "*"
    week: Union[Text, None] = "*"
    day: Union[Text, None] = "*"
    day_of_week: Union[Text, None] = "*"
    hour: Union[Text, None] = "*"
    minute: Union[Text, None] = "*"
    second: Union[Text, None] = "*"
    start_date: Union[Text, None] = None
    end_date: Union[Text, None] = None
    timezone: Union[Text, None] = None
    jitter: Union[int, None] = None


class IntervalTriggerModel(BaseModel):
    weeks: Union[Text, None] = None
    days: Union[Text, None] = None
    hours: Union[Text, None] = None
    minutes: Union[Text, None] = None
    seconds: Union[Text, None] = None
    start_date: Union[Text, None] = None
    end_date: Union[Text, None] = None
    timezone: Union[Text, None] = None
    jitter: Union[int, None] = None


class DateTriggerModel(BaseModel):
    run_date: Union[Text, None] = None
    timezone: Union[Text, None] = None
