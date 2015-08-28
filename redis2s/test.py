# Created by zhangwei7@baixing.com on 2015-08-28 13:22

import unittest

from redis2s.base import Base
from redis2s.cache import Cache
from redis2s.counter import DailyCounter


class TestRedis2s(unittest.TestCase):

    def test_get_tool_name(self):
        ret = Base().get_tool_name()
        self.assertEqual(ret, 'default')

    def test_rdb(self):
        ret = Base().rdb
        print(ret)

    def test_cache(self):
        cache = Cache('test')
        cache.set('123')
        self.assertEqual(cache.value(), '123')
        cache.delete()
        self.assertEqual(cache.value(), None)

    def test_daily_counter(self):
        c = DailyCounter('test')
        self.assertEqual(c.hit(), 1)
        self.assertEqual(c.value(), 1)
        c.delete()
        self.assertEqual(c.value(), 1)
