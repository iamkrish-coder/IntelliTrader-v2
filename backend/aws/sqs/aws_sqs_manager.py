import boto3
import uuid

from boto3.session import botocore
from botocore.exceptions import ClientError
from .aws_sqs_create_queue import CreateQueue
from .aws_sqs_delete_queue import DeleteQueue
from .aws_sqs_list_queues import ListQueues
from .aws_sqs_get_queue import GetQueue
from .aws_sqs_purge_queue import PurgeQueue
from .aws_sqs_publish_queue import PublishQueue
from .aws_sqs_subscribe_queue import SubscribeQueue
from .aws_sqs_delete_message_queue import DeleteMessageQueue


class SQSManager:
    def __init__(self):
        self.actions = {
            "create_queue": CreateQueue,
            "delete_queue": DeleteQueue,
            "list_queues": ListQueues,
            "get_queue": GetQueue,
            "purge_queue": PurgeQueue,
            "publish_queue": PublishQueue,
            "subscribe_queue": SubscribeQueue,
            "delete_message_queue": DeleteMessageQueue
        }

    def get_action(self, action_type, **kwargs):
        action_class = self.actions.get(action_type)
        if not action_class:
            raise ValueError(f"Invalid SQS action: {action_type}")

        return action_class(**kwargs)
