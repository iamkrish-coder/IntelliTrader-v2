import redis
from backend.utils.logging_utils import *


class RedisSubscriber:
    def __init__(self, queue, callback):
        self.queue = queue
        self.callback = callback
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(**{self.queue: self.handle_message})

    def handle_message(self, message):
        data = message['data'].decode('utf-8')
        self.callback(self.queue, data)

    def listen_for_messages(self):
        try:
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    self.handle_message(message)
        except Exception as error:
            log_error(f"An error occurred while listening for messages: {str(error)}")

    def stop_subscription(self):
        self.pubsub.unsubscribe(self.queue)
        self.pubsub.close()
        self.redis_client.close()
