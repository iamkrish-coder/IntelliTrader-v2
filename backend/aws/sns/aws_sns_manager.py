import boto3
import uuid

from boto3.session import botocore
from botocore.exceptions import ClientError
from .aws_sns_create_topic import CreateTopic
from .aws_sns_delete_topic import DeleteTopic
from .aws_sns_list_subscriptions import ListSubscriptions
from .aws_sns_list_topics import ListTopics
from .aws_sns_publish_topic import PublishTopic
from .aws_sns_subscribe_topic import SubscribeTopic
from .aws_sns_unsubscribe_topic import UnsubscribeTopic


class SNSManager:
    def __init__(self):
        self.actions = {
            "create_topic": CreateTopic,
            "delete_topic": DeleteTopic,
            "list_subscriptions": ListSubscriptions,
            "list_topics": ListTopics,
            "publish_topic": PublishTopic,
            "subscribe_topic": SubscribeTopic,
            "unsubscribe_topic": UnsubscribeTopic
        }

    def get_action(self, action_type, **kwargs):
        action_class = self.actions.get(action_type)
        if not action_class:
            raise ValueError(f"Invalid SNS action: {action_type}")

        return action_class(**kwargs)
