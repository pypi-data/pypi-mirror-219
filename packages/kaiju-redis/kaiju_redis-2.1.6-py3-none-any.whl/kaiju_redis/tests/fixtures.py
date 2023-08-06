import pytest  # noqa: pycharm

from kaiju_tools.docker import DockerContainer, DockerImage
from kaiju_tools.streams import Topic
from kaiju_tools.tests.fixtures import get_app

from kaiju_redis.services import *

__all__ = [
    'redis',
    'redis_glob',
    'redis_cache',
    'redis_locks',
    'redis_listener',
    'redis_client',
    'redis_transport',
    'REDIS_PORT',
]

REDIS_PORT = 6399


def _redis_container(app):
    return DockerContainer(
        app=app,
        image=DockerImage(app=app, tag='eqalpha/keydb', version='latest'),
        name='pytest-redis',
        ports={'6379': str(REDIS_PORT)},
        healthcheck={
            'test': "echo 'INFO' | keydb-cli",
            'interval': 100000000,
            'timeout': 3000000000,
            'start_period': 1000000000,
            'retries': 3,
        },
        sleep_interval=1,
        remove_on_exit=True,
    )


@pytest.fixture
def redis(app):
    """Get a new redis container."""
    with _redis_container(app) as c:
        yield c


@pytest.fixture(scope='session')
def redis_glob(logger):
    """Get a new redis container."""
    app = get_app(logger)
    with _redis_container(app) as c:
        yield c


@pytest.fixture
def redis_transport(redis_glob, app) -> RedisTransportService:
    """Get redis transport."""
    service = RedisTransportService(app=app, host='localhost', port=REDIS_PORT)
    app.services.add_service(service)
    return service


@pytest.fixture
def redis_cache(app, redis_transport) -> RedisCacheService:
    """Get redis cache."""
    service = RedisCacheService(app=app, transport=redis_transport)
    app.services.add_service(service)
    return service


@pytest.fixture
def redis_locks(app, redis_transport, scheduler) -> RedisLocksService:
    """Get locks class."""
    service = RedisLocksService(app=app, transport=redis_transport, scheduler=scheduler)
    app.services.add_service(service)
    return service


@pytest.fixture
def redis_listener(app, rpc, mock_sessions, mock_auth, scheduler, mock_locks, redis_transport) -> RedisListener:
    """Get stream listener class."""
    service = RedisListener(
        app=app,
        topic=Topic.RPC,
        transport=redis_transport,
        rpc_service=rpc,
        scheduler=scheduler,
        session_service=mock_sessions,
        authentication_service=mock_auth,
        locks_service=mock_locks,
        max_batch_size=1,
        max_wait_time_ms=50,
        scope='SYSTEM',
    )
    app.services.add_service(service)
    return service


@pytest.fixture
def redis_client(app, redis_transport, mock_users) -> RedisStreamRPCClient:
    """Get stream listener class."""
    service = RedisStreamRPCClient(
        app=app,
        app_name=app.name,
        topic=Topic.RPC,
        request_logs=True,
        response_logs=True,
        transport=redis_transport,
        auth_str=f'Basic {mock_users.username}:{mock_users.password}',
    )
    app.services.add_service(service)
    return service
