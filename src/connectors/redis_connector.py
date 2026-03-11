import redis.asyncio as redis


class RedisConnector:
    def __init__(self, host, port, password=None):
        self.port = port
        self.host = host
        self.password = password
        self.redis = None

    async def connect(self):
        params = {"host": self.host, "port": self.port, "decode_responses": True}
        if self.password:
            params["password"] = self.password

        self.redis = redis.Redis(**params)

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()
