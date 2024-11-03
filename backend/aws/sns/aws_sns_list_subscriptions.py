import boto3

from botocore.exceptions import ClientError
from .BaseSnsManager import BaseSnsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class ListSubscriptions(BaseSnsManager):
    """Encapsulates Amazon SNS topic."""

    def __init__(self, topic_arn=None, next_token=None):
        """
        :param sns_client_resource: A Boto3 Amazon SNS client resource.
        """
        self.sns_client = boto3.client(SNS, region_name=REGION_NAME)
        self.topic_arn = topic_arn
        self.next_token = next_token

    def execute(self):
        """
        Lists subscriptions for the current account, optionally limited to a
        specific topic.

        :param topic: When specified, only subscriptions to this topic are returned.
        :return: An iterator that yields the subscriptions.
        """
        try:
            if self.topic_arn is None:
                if self.next_token is not None:
                    response = self.sns_client.list_subscriptions(NextToken=self.next_token)
                else:
                    response = self.sns_client.list_subscriptions()
            else:
                response = self.sns_client.list_subscriptions_by_topic(TopicArn=self.topic_arn)
        except ClientError as error:
            log_error("Couldn't get subscriptions.")
            raise error
        else:
            return response
