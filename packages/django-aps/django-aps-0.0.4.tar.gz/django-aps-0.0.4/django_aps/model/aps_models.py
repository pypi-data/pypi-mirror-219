"""
APScheduler models
"""
from __future__ import annotations

import datetime
from typing import Union, Text, Dict, List, Any

import typing_extensions
from pydantic import BaseModel
from typing_extensions import Literal

IncEx: typing_extensions.TypeAlias = 'set[int] | set[str] | dict[int, Any] | dict[str, Any] | None'


class APSchedulerJob(BaseModel):
    id: Text
    name: Text
    func_ref: Text
    func_module: Union[Text, None] = None
    func_name: Union[Text, None] = None
    trigger: Any
    func_args: Union[List, None]
    func_kwargs: Union[Dict, None]
    next_run_time: Union[None, datetime.datetime]

    # status: Union[Text, None] = None

    def model_dump(
            self,
            *,
            mode: Literal['json', 'python'] | str = 'python',
            include: IncEx = None,
            exclude: IncEx = None,
            by_alias: bool = False,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool = True,
    ) -> dict[str, Any]:
        self.parse_func_model_name()
        self.parse_trigger()
        return super().model_dump(mode=mode, include=include, exclude=exclude, by_alias=by_alias,
                                  exclude_unset=exclude_unset, exclude_defaults=exclude_defaults,
                                  exclude_none=exclude_none, round_trip=round_trip, warnings=warnings)

    def parse_func_model_name(self):
        self.func_module, self.func_name = self.func_ref.split(':')

    def parse_trigger(self):
        if isinstance(self.trigger, dict):
            return
        trigger_dict = {}
        for field in self.trigger.fields:
            if field.is_default:
                continue
            trigger_dict.setdefault(field.name, str(field))
        self.trigger = trigger_dict
