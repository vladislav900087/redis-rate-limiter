from app.redis_client import redis_client


COUNT_REQUEST = """
local count = redis.call('INCR', KEYS[1])
if count == 1 then
    redis.call('EXPIRE', KEYS[1], 60)
end

return {count, redis.call('TTL', KEYS[1])}

"""


def get_retry_after(ip: str) -> int | None:

    count, seconds = redis_client.eval(COUNT_REQUEST, 1, f'rate_limit:{ip}')

    if count > 5:
        return max(1, seconds)

    return None