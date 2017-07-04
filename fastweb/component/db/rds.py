# coding:utf8

import redis
import shlex

import tornadis
from tornadis.exceptions import ConnectionError as torConnectionError
from redis.exceptions import ConnectionError, TimeoutError, ResponseError

from fastweb.accesspoint import coroutine, Return

import fastweb.util.tool as tool
from fastweb.exception import RedisError
from fastweb.component import Component


DEFAULT_DB = 0
DEFAULT_PORT = 6379
DEFAULT_TIMEOUT = 5
DEFAULT_CHARSET = 'utf8'


class Redis(Component):
    """Redis基类"""

    eattr = {'host': str}
    oattr = {'port': int, 'password': str, 'db': int, 'timeout': int, 'charset': str}

    def __init__(self, setting):
        self.db = DEFAULT_DB
        self.port = DEFAULT_PORT
        self.timeout = DEFAULT_TIMEOUT
        self.charset = DEFAULT_CHARSET

        super(Redis, self).__init__(setting)

        self._client = None

    @staticmethod
    def _parse_response(response):
        """解析response"""

        if response == 'OK':
            return True
        elif isinstance(response, tornadis.ClientError):
            raise RedisError(response)
        else:
            return response

    def reconnect(self):
        pass

    def ping(self):
        pass


class SyncRedis(Redis):
    """同步redis
       线程不安全"""

    def __str__(self):
        return '<SyncRedis {name} {host} {port} {db} {charset}>'.format(
            name=self.name, host=self.host, port=self.port, db=self.db, charset=self.charset)

    def connect(self):
        self.setting['socket_timeout'] = self.setting.pop('timeout', None)

        try:
            self.recorder('INFO', '{obj} connect start'.format(obj=self))
            self._client = redis.StrictRedis(**self.setting)
            self.recorder('INFO', '{obj} connect successful'.format(obj=self))
        except ConnectionError as e:
            self.recorder('ERROR', '{obj} connect failed [{msg}]'.format(obj=self, msg=e))
            raise RedisError
        return self

    def query(self, command):
        """命令行操作
           ConnectionError可能是超出连接最大数
           TimeoutError可能是连接不通"""

        try:
            cmd = shlex.split(command)
            self.recorder('INFO', '{obj} query start\n{cmd}'.format(obj=self, cmd=command))
            with tool.timing('s', 10) as t:
                response = self._client.execute_command(*cmd)
            self.recorder('INFO', '{obj} query successful\n{cmd} -- {time}'.format(obj=self, cmd=command, time=t))
        except (ConnectionError, TimeoutError) as e:
            # redis内部对这两种异常进行了重试操作
            self.recorder('ERROR', '{obj} connection error [{msg}]'.format(obj=self, msg=e))
            raise RedisError
        except ResponseError as e:
            self.recorder('ERROR', '{obj} query error [{msg}]'.format(obj=self, msg=e))
            raise RedisError

        return self._parse_response(response)


class AsynRedis(Redis):
    """异步redis组件"""

    def __str__(self):
        return '<AsynRedis {name} {host} {port} >'.format(
            host=self.host, port=self.port, name=self.name)

    @coroutine
    def connect(self):
        self.setting['connect_timeout'] = self.setting.pop('timeout', None)
        self.setting.pop('charset', None)

        try:
            self.recorder('INFO', '{obj} connect start'.format(obj=self))
            self._client = tornadis.Client(**self.setting)
            future = yield self._client.connect()
            if not future:
                raise RedisError
            self.recorder('INFO', '{obj} connect successful'.format(obj=self))
        except torConnectionError as e:
            self.recorder('ERROR', '{obj} connect failed [{msg}]'.format(obj=self, msg=e))
            raise RedisError
        raise Return(self)

    @coroutine
    def query(self, command):
        """执行redis命令"""

        try:
            cmd = shlex.split(command)
            self.recorder('INFO', '{obj} query start\nCommand: {cmd}'.format(obj=self, cmd=command))
            with tool.timing('s', 10) as t:
                response = yield self._client.call(*cmd)
            self.recorder('INFO', '{obj} query success\nCommand: {cmd}\nResponse: {res} -- {time}'.format(obj=self,
                                                                                                          cmd=command,
                                                                                                          res=response,
                                                                                                          time=t))
        except torConnectionError as e:
            self.recorder('ERROR', '{obj} connection error [{msg}]'.format(obj=self, msg=e))
            raise RedisError

        raise Return(self._parse_response(response))


