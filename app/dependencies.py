from fastapi import Depends, HTTPException, Request
from redis.exceptions import ConnectionError, TimeoutError

from app.limiter import get_retry_after


def enforce_rate_limit(request: Request) -> None:
    try:
        retry_after = get_retry_after(request.client.host)
    except (ConnectionError, TimeoutError) as exc:
        raise HTTPException(status_code=503, detail='Redis is unavailable') from exc

    if retry_after is not None:
        raise HTTPException(status_code=429, detail=f'Too many requests. Try again in {retry_after} seconds.', headers={'Retry-After': str(retry_after)})