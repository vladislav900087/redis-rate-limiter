from fastapi import Depends, HTTPException, Request, status
from redis.exceptions import ConnectionError, TimeoutError
from app.limiter import get_retry_after


def enforce_rate_limit(request: Request):

    try:
        retry_after = get_retry_after(request.client.host)
    except (ConnectionError, TimeoutError):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Redis is not available')

    if retry_after:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f'Too many requests. Try again in {retry_after} seconds', headers={'Retry-After': str(retry_after)})
