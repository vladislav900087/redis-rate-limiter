from app.redis_client import redis_client
from fastapi.testclient import TestClient
from app.main import app
from redis.exceptions import ConnectionError, TimeoutError

def test_read_root(client):

    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_ping(client):

    response = client.get('/ping')

    assert response.status_code == 200

    assert response.json() == {'message': 'pong'}

def test_sixth_request_returns_429(client):

    key = "rate_limit:testclient"

    redis_client.delete(key)

    try:
        for _ in range(5):
            response = client.get('/ping')
            assert response.status_code == 200

        response = client.get('/ping')
        assert response.status_code == 429

        seconds = int(response.headers['Retry-After'])

        assert 1 <= seconds <= 60

        assert f'Try again in {seconds} seconds' in response.json()['detail']

    finally:
        redis_client.delete(key)

def test_further_requests_do_not_restart_timer(client):

    key = 'rate_limit:testclient'

    redis_client.delete(key)

    try:
        response = client.get('/ping')
        assert response.status_code == 200

        assert redis_client.expire(key, 30)
        deadline = redis_client.pexpiretime(key)

        assert deadline > 0



        for _ in range(4):
            assert client.get('/ping').status_code == 200

        response = client.get('/ping')
        assert response.status_code == 429
        seconds = int(response.headers['Retry-After'])

        assert 1 <= seconds <= 60

        response = client.get('/ping')

        seconds = int(response.headers['Retry-After'])

        assert response.status_code == 429
        assert redis_client.pexpiretime(key) == deadline

    finally:
        redis_client.delete(key)


def test_ip_isolation(client):

    ip_a = '192.0.2.1'
    ip_b = '192.0.2.2'

    keys = (f'rate_limit:{ip_a}', f'rate_limit:{ip_b}')

    redis_client.delete(*keys)

    try:
        for ip in (ip_a, ip_b):
            with TestClient(app, client=(ip, 50000)) as client:
                for _ in range(5):
                    response = client.get('/ping')
                    assert response.status_code == 200

                response = client.get('/ping')
                assert response.status_code == 429

    finally:
        redis_client.delete(*keys)


def test_redis_unavailable_returns_503(client, monkeypatch):

    def fail(*args):
        raise ConnectionError('Redis is unavailable')

    monkeypatch.setattr(redis_client, "eval", fail)

    assert client.get('/ping').status_code == 503

def test_redis_timeout_returns_503(client, monkeypatch):

    def fail(*args):
        raise TimeoutError('Redis is unavailable')

    monkeypatch.setattr(redis_client, 'eval', fail)

    assert client.get('/ping').status_code == 503






