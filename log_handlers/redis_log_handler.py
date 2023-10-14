import logging
import redis
import redis.asyncio as async_redis


class RedisSyncHandler(logging.Handler):
    """
    Publish messages to redis channel.
    """

    def __init__(
        self,
        channel,
        level=logging.INFO
    ):
        """
        Create a new logger for the given channel and redis_client.
        """
        logging.Handler.__init__(self, level)
        self.channel = channel
        self.redis_client = redis.Redis(host='redis')

    def emit(self, record):
        """
        Publish record to redis logging channel
        """
        try:
            self.redis_client.publish(self.channel, self.format(record))
        except redis.RedisError:
            self.redis_client.close()
            raise


class RedisAsyncHandler(logging.Handler):
    """
    Publish messages to redis channel.
    """

    def __init__(
        self,
        channel,
        level=logging.INFO
    ):
        """
        Create a new logger for the given channel and redis_client.
        """
        logging.Handler.__init__(self, level)
        self.channel = channel
        self.redis_client = async_redis.Redis(host='redis')

    def emit(self, record):
        """
        Publish record to redis logging channel
        """
        try:
            self.redis_client.publish(self.channel, self.format(record))
        except redis.RedisError:
            self.redis_client.close()
            raise
