#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      loc_mem_cache
   Description:
   Author:          dingyong.cui
   date：           2023/7/11
-------------------------------------------------
   Change Activity:
                    2023/7/11
-------------------------------------------------
"""
import time
from typing import Any

from django.core.cache.backends.locmem import LocMemCache


class CustomLocMemCache(LocMemCache):

    def ttl(self, key: Any):
        key = self.make_key(key)
        self.validate_key(key)
        with self._lock:
            return self._expire_info.get(key, -1) - time.time()
