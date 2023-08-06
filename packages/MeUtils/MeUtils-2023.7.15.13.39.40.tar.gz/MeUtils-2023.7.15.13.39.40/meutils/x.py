#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2023/7/6 20:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.cache_utils import diskcache


class A:

    @classmethod
    @diskcache(verbose=111)
    def f(cls, a):
        return a

