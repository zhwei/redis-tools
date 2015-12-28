# Created by zhwei on 2015-08-17 07:22
# 每次自增，不重置过期时间

from .base import Base


class Firewall(Base):

    def __init__(self, name, limit, expire=600):

        self.name = name
        self.limit = limit

        self.__last_value = 0
        self.__expire = expire
        self.__key = self.get_key(name)

    def hit(self, count=1):
        self.__last_value = int(self.rdb.incr(self.__key, count))
        return self.__last_value > self.limit

    def last_value(self):
        return self.__last_value

    def value(self):
        v = self.rdb.get(self.__key)
        return int(v) if v else 0

    def is_blocked(self):
        return self.value() > self.limit

    def refresh(self):
        return self.rdb.expire(self.__key, self.__expire)

    def reset(self):
        return self.rdb.delete(self.__key)
