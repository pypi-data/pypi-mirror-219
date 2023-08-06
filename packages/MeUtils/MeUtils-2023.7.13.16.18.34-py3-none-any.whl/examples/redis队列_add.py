#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : redis队列
# @Time         : 2023/6/9 15:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
# from MeUtils.examples.redis队列 import queue
from rq import Queue
from redis import Redis

from MeUtils.examples.demo import fn

queue = Queue(connection=Redis())
r = queue.enqueue(fn, 1).return_value

print('结果：', r)

