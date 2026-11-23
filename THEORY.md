# Main definitions

## Redis:

### Definition:
- Redis is a database that keeps data in memory for fast reads and writes.

### How it is used in Redis Rate Limiter API:
- The API uses it to store a request counter for each API address.

## INCR:

### Definition:
- INCR is a Redis command that adds 1 to a stored number and returns the new number.

### How it is used in Redis Rate Limiter API:
- The API uses it to count requests.

## TTL:

### Definition:
- TTL is the time left before Redis automatically deletes a stored entry

### How it is used in Redis Rate Limiter API:
- Give each counter an expiration so an IP gets a fresh allowance when its time window ends

## IP Address:

### Definition:
- IP Address is a numeric address used to send data to the right place on the network.

### How it is used in Redis Rate Limiter API:
- The API uses it to group requests by client IP it sees. Requests with the same IP share one counter.

## 429 Too many requests:

### Definition:
- The client sent too many requests in a given time.

### How it is used in Redis Rate Limiter API:
- The API uses it to limit the HTTP-request frequency.

## 503 Service Unavailable:

### Definition:
- The server is temporarily unable to handle the request.

### How it is used in Redis Rate Limiter API:
- The API uses it to message that Redis is unreachable and the limits cannot be checked.







