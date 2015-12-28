# Created by zhwei on 2015-03-12 15:42
# 计数器，每次hit后重置超时时间

import time

from .base import Base


class Counter(Base):

    def __init__(self, name, expire=3600 * 24 * 7):
        """
        :param name: 计数器名
        :param expire: 超时事件，默认七天
        """
        self.__expire = expire
        self.__key = self.get_key(name)

    def hit(self, count=1):
        """ 自增
        :param count: 增量, 默认为1
        :return 自增后的值
        """
        count = self.rdb.incr(self.__key)
        self.rdb.expire(self.__key, self.__expire)
        return count

    def value(self):
        val = self.rdb.get(self.__key)
        return 0 if not val else int(val)


class DailyCounter(Base):
    """ 自动按天区分, 用来出报表
    """
    def __init__(self, name, expire=3600 * 24 * 7):
        self.name = name

        self.__expire = expire
        self.__key = self.get_key(time.strftime('%Y%m%d'))

    def hit(self, count=1):
        return int(self.rdb.hincrby(self.__key, self.name, count))

    def value(self):
        return int(self.rdb.hget(self.__key, self.name) or 0)

    def delete(self):
        return self.rdb.hdel(self.__key, self.name)