import redis


class RedisPublisher:
    def __init__(self, queue):
        self.queue = queue
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def publish_message(self, message):
        self.redis_client.publish(self.queue, message)
