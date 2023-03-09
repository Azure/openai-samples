# RediSearch with Docker

Use the provided Docker Compose file to set up a Redis database:
```bash
$ docker compose up
```

> add `-d` to the command to daemonize the process to the background.

### Connecting to Redis

If you're connecting to Redis from an app in the same Docker network, use the following:
```python
import os
import redis

# Connect to Redis from an app in the same Docker network
redis_conn = redis.Redis(
    host="redis",
    port=6379,
    #password=<your-redis-password>
)
```

> Otherwise, if on the host machine's network, use `localhost` as the redis host param.

### Shutting Down

```bash
$ docker compose down
```