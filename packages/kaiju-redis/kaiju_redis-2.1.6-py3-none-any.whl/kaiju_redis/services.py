"""Redis services."""

import textwrap
from typing import Collection, FrozenSet, Type, List

from coredis import Redis, RedisCluster  # noqa: pycharm
from coredis.exceptions import ResponseError, StreamConsumerGroupError  # noqa: pycharm

from kaiju_tools.app import ContextableService, SERVICE_CLASS_REGISTRY
from kaiju_tools.cache import BaseCacheService
from kaiju_tools.encoding import msgpack_dumps, msgpack_loads
from kaiju_tools.functions import retry
from kaiju_tools.locks import BaseLocksService, NotLockOwnerError, LockExistsError
from kaiju_tools.streams import StreamRPCClient, Listener
from kaiju_tools.types import NSKey

__all__ = ['RedisTransportService', 'RedisCacheService', 'RedisLocksService', 'RedisListener', 'RedisStreamRPCClient']


class RedisTransportService(ContextableService):
    """Redis transport."""

    transport_class = Redis
    cluster_transport_class = RedisCluster

    def __init__(
        self,
        app,
        *args,
        cluster: bool = False,
        connect_timeout: int = 30,
        max_idle_time: int = 60,
        retry_on_timeout=True,
        logger=None,
        **kws,
    ):
        """Initialize.

        :param app:
        :param args: additional transport cls args
        :param cluster: use cluster connector class
        :param connect_timeout: connection timeout
        :param max_idle_time: max connection idle time
        :param retry_on_timeout: retry connection on timeout
        :param logger:
        :param kws: additional transport cls args
        """
        super().__init__(app, logger=logger)
        if cluster:
            cls = self.cluster_transport_class
        else:
            cls = self.transport_class
        self._transport = cls(
            *args,
            connect_timeout=connect_timeout,
            max_idle_time=max_idle_time,
            retry_on_timeout=retry_on_timeout,
            **kws,
        )

    def __getattr__(self, item):
        return getattr(self._transport, item)

    async def init(self):
        self.connection_pool.reset()

    async def close(self):
        self.connection_pool.disconnect()


class RedisCacheService(BaseCacheService):
    """Provides caching via Redis or KeyDB."""

    M_SET_EXP_SCRIPT = """
    local ttl = ARGV[1]
    for i, key in pairs(KEYS) do
        redis.call('SETEX', key, ttl, ARGV[i + 1])
    end
    """

    M_EXISTS_SCRIPT = """
    local result = {}
    for i, key in pairs(KEYS) do
        result[i] = redis.call('EXISTS', key)
    end
    return result
    """

    _m_set_exp_script = None  #: compiled script
    _m_exists_script = None  #: compiled script
    _transport: RedisTransportService

    async def init(self):
        await super().init()
        self._m_set_exp_script = self._transport.register_script(textwrap.dedent(self.M_SET_EXP_SCRIPT))
        self._m_exists_script = self._transport.register_script(textwrap.dedent(self.M_EXISTS_SCRIPT))

    @classmethod
    def get_transport_cls(cls) -> Type:
        return RedisTransportService

    async def exists(self, id: NSKey) -> bool:
        existing = await self._transport.exists([id])
        return bool(existing)

    async def m_exists(self, id: Collection[NSKey]) -> FrozenSet[str]:
        keys = await self._m_exists_script.execute(keys=id)
        return frozenset(key for key, value in zip(id, keys) if bool(value))

    async def _get(self, key: str):
        return await self._transport.get(key)

    async def _m_get(self, *keys: str):
        return await self._transport.mget(keys)

    async def _set(self, key: str, value, ttl: int):
        if ttl:
            return await self._transport.setex(key, value, ttl)
        else:
            return await self._transport.set(key, value)

    async def _m_set(self, keys: dict, ttl: int):
        if ttl:
            return await self._m_set_exp_script.execute(keys=list(keys.keys()), args=[ttl, *list(keys.values())])
        else:
            return await self._transport.mset(keys)

    async def _delete(self, key: str):
        return await self._transport.delete([key])

    async def _m_delete(self, *keys: str):
        self.logger.info('DELETE')
        try:
            await self._transport.delete(keys)
        except Exception as exc:
            self.logger.info(str(exc))
        self.logger.info('OK')

    async def lpush(
        self,
        key: NSKey,
        *values,
    ) -> None:
        """Set a list data into list.

        :param key: string only
        :param values: list of serializable value
        """
        self.logger.info('Add key "%s"', key)
        values = [self._dump_value(v) for v in values]
        await self._transport.lpush(key, values)

    async def rpush(self, key: NSKey, *values) -> None:
        """Set a list data into list.

        :param key: string only
        :param values: list of serializable value
        """
        self.logger.info('Add key "%s"', key)
        values = [self._dump_value(v) for v in values]
        await self._transport.rpush(key, values)

    async def llen(self, key: NSKey) -> int:
        """Get count of list.

        :param key: string only
        """
        self.logger.info('Get key count "%s"', key)
        return await self._transport.llen(key)

    async def lrange(self, key: NSKey, start=0, end=10):
        """Get values from list by key.

        :param key: string only
        :param start: positive int only
        :param end: positive int only
        """
        self.logger.info('Set range for key %s .', key)
        values = await self._transport.lrange(key, start=start, stop=end)
        if values:
            values = [self._load_value(v) for v in values]
        return values

    async def lpop(self, key: NSKey):
        """Get values from list by key.

        :param key: string only
        """
        self.logger.info('Set range for key %s .', key)
        value = await self._transport.lpop(key)
        if value:
            value = self._load_value(value)
        return value


class RedisLocksService(BaseLocksService):
    """Locks service with Redis backend."""

    class ErrorCode:
        """Error codes used by redis scripts."""

        OK = 'OK'
        LOCK_EXISTS = 'LOCK_EXISTS'
        NOT_LOCK_OWNER = 'NOT_LOCK_OWNER'

    LOCK_SCRIPT = f"""
    local e = redis.call('get', KEYS[1])
    if not e then
        redis.call('set', KEYS[1], ARGV[1])
        redis.call('expire', KEYS[1], ARGV[2])
        return redis.status_reply('{ErrorCode.OK}')
    else
        return redis.error_reply('{ErrorCode.LOCK_EXISTS}')
    end"""

    UNLOCK_SCRIPT = f"""
    local _id = redis.call('get', KEYS[1])
    if _id == ARGV[1] then
        redis.call('del', KEYS[1])
        return redis.status_reply('{ErrorCode.OK}')
    elseif not _id then
        return redis.status_reply('{ErrorCode.OK}')
    else
        return redis.error_reply('{ErrorCode.NOT_LOCK_OWNER}')
    end"""

    RENEW_SCRIPT = """
    for i, key in pairs(KEYS) do
        redis.call('expire', key, ARGV[i])
    end
    """

    EXISTS_SCRIPT = RedisCacheService.M_EXISTS_SCRIPT
    _lock_script = None
    _unlock_script = None
    _renew_script = None
    _exists_script = None
    _transport: RedisTransportService

    async def init(self):
        await super().init()
        self._lock_script = self._transport.register_script(textwrap.dedent(self.LOCK_SCRIPT))
        self._unlock_script = self._transport.register_script(textwrap.dedent(self.UNLOCK_SCRIPT))
        self._renew_script = self._transport.register_script(textwrap.dedent(self.RENEW_SCRIPT))
        self._exists_script = self._transport.register_script(textwrap.dedent(self.EXISTS_SCRIPT))

    @classmethod
    def get_transport_cls(cls) -> Type:
        return RedisTransportService

    async def m_exists(self, keys: List[NSKey]) -> FrozenSet[NSKey]:
        data = await self._exists_script.execute(keys=keys)
        if data:
            return frozenset(key for key, value in zip(keys, data) if bool(value))
        else:
            return frozenset()

    async def _acquire(self, keys: list, identifier: str, ttl: int):
        try:
            await self._lock_script.execute(keys=keys, args=[identifier, int(ttl)])
        except ResponseError as exc:
            if str(exc) == self.ErrorCode.LOCK_EXISTS:
                exc = LockExistsError(self.ErrorCode.LOCK_EXISTS)
            raise exc

    async def _release(self, keys: list, identifier: str):
        try:
            await self._unlock_script.execute(keys=keys, args=[identifier])
        except ResponseError as exc:
            if str(exc) == self.ErrorCode.NOT_LOCK_OWNER:
                exc = NotLockOwnerError(self.ErrorCode.NOT_LOCK_OWNER)
            raise exc

    async def _renew(self, keys: list, values: list):
        await self._renew_script.execute(keys=keys, args=[int(v) for v in values])

    async def _owner(self, key: str):
        owner = await self._transport.get(key)
        if owner:
            owner = owner.decode('utf-8')
            return owner


class RedisListener(Listener):
    """Redis stream listener."""

    _transport: RedisTransportService
    _loads = msgpack_loads
    _trim_interval = 300  # s
    _trim_op = b'~'  # either ~ or =

    def __init__(
        self,
        *args,
        group_id: str = None,
        consumer_id: str = None,
        max_batch_size: int = 10,
        max_wait_time_ms: int = 500,
        pending_messages_time_ms: int = None,
        trim_size: int = 100000,
        **kws,
    ):
        """Initialize.

        :param group_id: consumer group, `app.name` by default
        :param consumer_id: unique instance id, `app.id` by default
        :param max_batch_size: max single acquired batch size
        :param max_wait_time_ms: max wait time when waiting for a batch
        :param pending_messages_time_ms: processing pending messages timeout in ms
            (messages not acked since this interval will be auto-claimed by this listener)
            set `None` to disable this behavior
        :param trim_size: stream records trim size: older records will be removed
            if the stream is longer than this value
            set `None` to disable this behavior
        """
        super().__init__(*args, **kws)
        self.group_id = group_id if group_id else self.app.name
        self.consumer_id = consumer_id if consumer_id else str(self.app.id)
        self.max_batch_size = max_batch_size
        self.max_wait_time_ms = max_wait_time_ms
        self.pending_messages_time_ms = pending_messages_time_ms
        self.trim_size = trim_size
        self._task_claim_pending = None
        self._task_trim_records = None

    async def init(self):
        await super().init()
        await self._create_group()
        if self.pending_messages_time_ms:
            interval = max(1, self.pending_messages_time_ms // 1000)
            self._task_claim_pending = self._scheduler.schedule_task(
                self._claim_pending, interval=interval, name=f'{self.service_name}._claim_pending'
            )
        if self.trim_size:
            self._task_trim_records = self._scheduler.schedule_task(
                self._trim_records, interval=self._trim_interval, name=f'{self.service_name}._trim_records'
            )

    async def close(self):
        if self._task_claim_pending:
            self._task_claim_pending.enabled = False
        if self._task_trim_records:
            self._task_trim_records.enabled = False
        await super().close()

    async def _create_group(self) -> None:
        self.logger.info('Creating group %s for stream %s', self.group_id, self._key)
        try:
            groups = await self._transport.xinfo_groups(self._key)
            self.logger.debug('groups: %s', groups)
        except ResponseError:
            groups, mk_stream = frozenset(), True
        else:
            groups, mk_stream = frozenset(group[b'name'].decode() for group in groups), False
        if self.group_id not in groups:
            result = await self._transport.xgroup_create(self._key, self.group_id, identifier='$', mkstream=mk_stream)
            self.logger.debug('group create: %s', result)

    def get_transport(self):
        return self.discover_service(self._transport, cls=RedisTransportService)

    async def _read_batch(self) -> list:
        try:
            batch = await self._transport.xreadgroup(
                self.group_id,
                self.consumer_id,
                count=self.max_batch_size,
                block=self.max_wait_time_ms,
                streams={self._key: '>'},
                noack=True,
            )
        except StreamConsumerGroupError:
            await self._create_group()
        else:
            if batch:
                batch = next(iter(batch.values()), None)  # first topic, there should only be a single topic
                return batch

    async def _claim_pending(self) -> None:
        """Claim pending messages."""
        await self._transport.xautoclaim(
            self._key, self.group_id, self.consumer_id, self.pending_messages_time_ms, justid=True
        )

    async def _trim_records(self) -> None:
        """Trim older records."""
        result = await self._transport.xtrim(
            self._key, trim_strategy=b'MAXLEN', threshold=self.trim_size, trim_operator=self._trim_op
        )
        self.logger.debug('trim: %s', result)

    async def _process_batch(self, batch: list) -> None:
        acks = []
        for row in batch:
            row_id, data = row
            data = self._loads(data[b'_'])
            await self._process_request(data)
            acks.append(row_id)
        if acks:
            await retry(
                self._transport.xack,
                args=(self._key, self.group_id),
                kws={'identifiers': acks},
                retries=5,
                retry_timeout=1.0,
                max_retry_timeout=10,
                logger=self.logger,
            )


class RedisStreamRPCClient(StreamRPCClient):
    """Redis stream client."""

    _transport: RedisTransportService
    _dumps = msgpack_dumps

    def get_transport(self):
        return self.discover_service(self._transport, cls=RedisTransportService)

    async def write(self, topic: NSKey, body, headers: dict = None, key=None) -> None:
        """Write data to the stream.

        :param topic: topic key
        :param body: rpc request body
        :param headers: request headers
        :param key: (optional) message id
        """
        await self._transport.xadd(topic, {b'_': self._dumps((body, headers))}, identifier=key if key else '*')


SERVICE_CLASS_REGISTRY.register(RedisTransportService)
SERVICE_CLASS_REGISTRY.register(RedisCacheService)
SERVICE_CLASS_REGISTRY.register(RedisLocksService)
SERVICE_CLASS_REGISTRY.register(RedisListener)
SERVICE_CLASS_REGISTRY.register(RedisStreamRPCClient)
