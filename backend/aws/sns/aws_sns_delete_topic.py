import boto3

from botocore.exceptions import ClientError
from .BaseSnsManager import BaseSnsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class DeleteTopic(BaseSnsManager):
    """Encapsulates Amazon SNS topic."""

    def __init__(self, topic_arn):
        """
        :param sns_client_resource: A Boto3 Amazon SNS client resource.
        """
        self.sns_client = boto3.client(SNS, region_name=REGION_NAME)
        self.topic_arn = topic_arn

    def execute(self):
        """
        Deletes a topic. All subscriptions to the topic are also deleted.
        """
        try:
            self.sns_client.delete_topic(TopicArn=self.topic_arn)
            log_info("Deleted topic %s.", self.topic_arn)
        except ClientError as error:
            log_error("Couldn't delete topic %s.", self.topic.arn)
            raise error
