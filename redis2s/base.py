# Created by zhwei on 2015-08-28 13:12

from . import client


class Base(object):

    PREFIX = 'redis2s:'

    @classmethod
    def get_tool_name(cls):
        cls_name = cls.__name__
        print(cls_name)
        if cls_name == 'Base':
            return 'default'

        return cls_name.lower()

    @property
    def rdb(self):
        if not hasattr(self, '_rdb'):
            config = None
            name = self.get_tool_name()
            for n, c in client.config.items():
                if (isinstance(n, (list, tuple)) and name in n) or name == n:
                    config = c
                    break

                continue

            if config is None:
                config = client.config.get('default')

            if config is None:
                raise RuntimeError('please set `default` or `{}`'.format(name))

            self._rdb = client.Client(host=config['host'], port=config['port'],
                                      db=config['db'])
        return self._rdb

    @classmethod
    def get_key(cls, name):
        return cls.PREFIX + cls.get_tool_name() + ':' + str(name)

    def delete(self):
        if hasattr(self, '__key'):
            self.rdb.delete(self.__key)

    def __delete__(self, instance):
        if hasattr(instance, 'delete'):
            instance.delete()
