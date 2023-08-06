import asyncio
import uuid

import pytest  # noqa: pycharm
import pytest_asyncio

from kaiju_tools.tests.test_cache import TestCache as TestCacheBase
from kaiju_tools.tests.test_locks import TestLocks as TestLocksBase
from kaiju_tools.tests.test_streams import TestStreamServer as TestStreamServerBase
from kaiju_tools.tests.test_streams import TestStreamClient as TestStreamClientBase

from kaiju_redis.services import RedisStreamRPCClient

__all__ = ['TestCache', 'TestLocks', 'TestStreamServer', 'TestStreamClient']


class _Queue:
    """Queue-like interface for streams."""

    def __init__(self, listener):
        self._listener = listener
        self._task = None

    def put_nowait(self, data):
        self._task = asyncio.create_task(self._write(data))

    async def _write(self, data):
        result = await self._listener._transport.xadd(
            self._listener._key, {b'_': RedisStreamRPCClient._dumps(data)}, identifier='*'
        )
        self._listener.logger.debug('write: %s', result)

    async def join(self):
        if self._task:
            await self._task
        await asyncio.sleep(self._listener.max_wait_time_ms * 2 / 1000)


@pytest.mark.asyncio
@pytest.mark.docker
async def test_redis_transport(redis_glob, redis_transport):
    log = await redis_transport.info()
    redis_transport.logger.debug(log)


@pytest.mark.docker
class TestCache(TestCacheBase):
    """Test redis cache."""

    @pytest_asyncio.fixture
    async def _cache(self, app, redis_cache):
        async with app.services:
            yield redis_cache
            await redis_cache._transport.flushdb()


@pytest.mark.docker
class TestLocks(TestLocksBase):
    """Test redis locks."""

    @pytest_asyncio.fixture
    async def _locks(self, app, redis_locks):
        redis_locks.WAIT_RELEASE_REFRESH_INTERVAL = 1
        redis_locks._refresh_interval = 1
        async with app.services:
            yield redis_locks
            await redis_locks._transport.flushdb()


@pytest.mark.docker
class TestStreamServer(TestStreamServerBase):
    """Test redis streams."""

    @pytest_asyncio.fixture
    async def _listener(self, app, redis_listener, mock_service, mock_sessions, mock_session):
        async with app.services:
            yield redis_listener
            await redis_listener._transport.flushdb()

    @pytest.fixture
    def _queue(self, redis_listener):
        return _Queue(redis_listener)

    async def test_redis_group_del_recovery(self, _queue, rpc, mock_service, _listener):
        result = await _listener._transport.xgroup_destroy(_listener._key, _listener.group_id)
        _listener.logger.debug(result)
        await asyncio.sleep(_listener.max_wait_time_ms * 3 / 1000)
        await self.test_valid_requests(rpc, _listener, _queue, mock_service)

    async def test_redis_key_del_recovery(self, _queue, rpc, mock_service, _listener):
        result = await _listener._transport.delete([_listener._key])
        _listener.logger.debug(result)
        await asyncio.sleep(_listener.max_wait_time_ms * 3 / 1000)
        await self.test_valid_requests(rpc, _listener, _queue, mock_service)

    async def test_redis_trim(self, _queue, rpc, mock_service, _listener):
        _listener.trim_size = 1
        _listener._trim_op = b'='
        for _ in range(10):
            _queue.put_nowait(({'method': 'do.echo'}, {}))
            await _queue.join()
        value = await _listener._transport.xlen(_listener._key)
        assert value == 10, 'before trim'
        await _listener._trim_records()
        value = await _listener._transport.xlen(_listener._key)
        assert value == 1, 'after trim'

    async def test_connection_issues(self, redis_glob, rpc, _listener, _queue, mock_service):
        redis_glob.pause()
        await asyncio.sleep(3)
        redis_glob.unpause()
        await _listener._transport.flushdb()
        await asyncio.sleep(1)
        await self.test_valid_requests(rpc, _listener, _queue, mock_service)


@pytest.mark.docker
class TestStreamClient(TestStreamClientBase):
    """Test redis stream client."""

    @pytest_asyncio.fixture
    async def _client(self, app, redis_listener, mock_service, mock_sessions, mock_session, redis_client):
        async with app.services:
            yield redis_client
            await redis_listener._transport.flushdb()

    @pytest.fixture
    def _queue(self, redis_listener):
        return _Queue(redis_listener)
