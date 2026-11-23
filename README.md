# Redis Rate Limiter

## Overview

Redis Rate Limiter is a component that protects API from overload by limiting the frequency of HTTP-requests.

## Features

- An API-route protected by a dependency that limits client's requests. If their quantity is above 5, the system raises the "429 Too many requests" error until 60 seconds expire.

## Tech stack

- Python
- FastAPI
- Redis
- Docker

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/vladislav900087/redis-rate-limiter
```

```bash
cd redis-rate-limiter
```

```bash
pip install -r requirements.txt -> installs dependencies locally.
```

```bash
pip install -r requirements.txt -> installs dependencies locally.
```

```bash
docker compose up -d --build -> builds and starts containers.

```


### Running the application:

```bash
docker compose up -d
```

## API Reference

```bash
GET /health -> health check
GET /ping -> a rate-limited endpoint
```

## Testing
```bash
pytest -v
```

## How it works

Each time the client sends a GET /ping request, the app sets a timer for 60 seconds and a counter incrementing it by 1. Reaching 6, 429 Too many requests is raised with remaining seconds shown until the time window expires. 

- INCR - increments counter in Redis
- EXPIRE - sets the timer
- TTL (Time to live) - remaining time in seconds



## License

MIT License © 2026 Vladislav




