#!/usr/bin/env python3
# Updated at 2015-03-26 11:27  by zhangwei7@baixing.com

import time

import redis


config = {
    'default': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }
}


class Client(redis.StrictRedis):
    REDIS_CONNS = {}

    def __init__(self, host='localhost', port=6379, db=0, hard_retry=5, **kwargs):
        """
        得到一个与 StrictRedis 兼容的 redis 客户端，具备连接数限制能力，以及对可恢复的错误的自动重试能力；

        一个 host + port 的组合，对应一个连接池，连接数的限制是在本进程内（俗称“一个 main 里面”），所以对于一个进程内的多线程
        导致的 too many clients 错误，是能够有效避免的；

        但即便是限制了每个组合对应的连接数，但在多进程情况下，整体连接数还是可能超过 redis server 的最大连接数；

        一个 host + port 的组合，其最大连接数 pool_max_connections 在第一次指定的时候的取值，是不能被修改的，修改也无效；
        经过测试，在密集使用 redis 的环境中，一个 host + port 的组合，pool_max_connections 取 3 至 5 已经足够，因为 redis
        本身是单线程处理请求的，过大的并发量没有意义；

        :param host: 目标 redis 服务器的机器名或地址，默认是 localhost；
        :param port: 目标 redis 服务器的端口，默认是 6379；
        :param db: 目标 redis 服务器的数据库编号，默认是 0；
        :return: 一个与 StrictRedis 兼容的 redis 客户端实例；
        """
        self.hard_retry = hard_retry
        self.conn_pool_key = (host, port, db)
        connection_pool = Client.REDIS_CONNS.get(self.conn_pool_key)
        if connection_pool:
            self.connection_pool = connection_pool
            self._use_lua_lock = None
            self.response_callbacks = self.__class__.RESPONSE_CALLBACKS.copy()
        else:
            super(Client, self).__init__(host=host, port=port, db=db, **kwargs)
            self.__class__.REDIS_CONNS[self.conn_pool_key] = self.connection_pool

    def execute_command(self, *args, **kwargs):
        result = None
        exec_finish = False
        hard_error_retry = 0
        while not exec_finish:
            try:
                result = super(Client, self).execute_command(*args, **kwargs)
                exec_finish = True
            except AttributeError:
                raise

            except (redis.ConnectionError, redis.ResponseError, redis.TimeoutError, redis.BusyLoadingError) as error:
                error_msg = str(error).lower().strip()
                print("[Client]: {}, {}".format(self.conn_pool_key, error_msg))
                time.sleep(1)
                hard_error_retry += 1

            except Exception:
                raise

            if hard_error_retry >= self.hard_retry:
                exec_finish = True  # hard error limit reached, force return None

        return result
