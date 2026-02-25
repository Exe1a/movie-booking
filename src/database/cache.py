from redis import Redis, ConnectionPool
from dotenv import dotenv_values
from fastapi import FastAPI, Request
from contextlib import contextmanager

redis_host = str(dotenv_values(".env").get("REDIS_HOST"))
redis_port = str(dotenv_values(".env").get("REDIS_PORT"))

@contextmanager
async def lifespan(app: FastAPI):
    redis_connection_pool = ConnectionPool(host=redis_host,
                                           port=redis_port,
                                           decode_respoense=True)
    redis_client = Redis(connection_pool=redis_connection_pool)
    app.state.redis = redis_client
    yield
    redis_client.close()

def get_redis(request: Request) -> Redis:
    return request.app.state.redis