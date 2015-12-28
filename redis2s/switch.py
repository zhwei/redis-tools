# Created by zhwei on 2015-04-21 18:04
# 开关

from .base import Base


class Switch(Base):

    def __init__(self, name, expire=86400 * 365):
        self.name = name
        self.__expire = expire
        self.__key = self.get_key(name)

    def turn_on(self, msg='on'):
        return self.rdb.setex(self.__key, self.__expire, msg)

    def turn_off(self):
        return self.rdb.delete(self.__key)

    def value(self):
        ret = self.rdb.get(self.__key)
        return ret.decode() if ret else None
