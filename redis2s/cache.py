# Created by zhangwei7@baixing.com on 2015-05-11 10:04

import pickle

from .base import Base


class Cache(Base):
    """ Just a Cache
    """

    def __init__(self, name, ttl=86400 * 7):
        """
        :param name: 缓存标记
        :param ttl: 过期时间，默认七天
        """
        self.name = name
        self.ttl = ttl

        self.__key = self.get_key(name)

    def value(self):
        raw = self.rdb.get(self.__key)
        if not raw:
            return None

        return pickle.loads(raw)

    def set(self, value):
        return self.rdb.setex(self.__key, self.ttl, pickle.dumps(value))
