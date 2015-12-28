# Created by zhwei on 2015-08-28 11:29


from redis2s.cache import Cache
from redis2s.switch import Switch
from redis2s.firewall import Firewall
from redis2s.client import config, Client
from redis2s.counter import Counter, DailyCounter


def set_key_prefix(prefix):
    """ default key prefix is `redis2s:` """

    from redis2s.base import Base
    Base.PREFIX = str(prefix)


""" config connections

redis2s.config = {

}

"""
