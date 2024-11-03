import boto3
import uuid

from botocore.exceptions import ClientError
from .BaseSqsManager import BaseSqsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class PublishQueue(BaseSqsManager):
    """Encapsulates Amazon SQS queue."""

    def __init__(self, mode, queue_url, message, attributes, receipt_handle):
        """
        :param sqs_client_resource: A Boto3 Amazon SQS client resource.
        """
        self.sqs_client = boto3.client(SQS, region_name=REGION_NAME)
        self.mode = mode
        self.queue_url = queue_url
        self.message = message
        self.attributes = attributes
        self.receipt_handle = receipt_handle

    def execute(self):
        """
        Publishes a message either Standard or FIFO mode, with attributes, to a topic. Subscriptions can be filtered
        based on message attributes so that a subscription receives messages only
        when specified attributes are present.
        """
        if self.mode == STANDARD:
            return self.publish_standard_queue()
        elif self.mode == FIFO:
            return self.publish_fifo_queue()

    def publish_standard_queue(self):
        try:
            response = True
            # Todo: Need queue publishing backend code (Not Implemented yet)

            log_info(
                "Published message with attributes %s to queue %s.",
                self.attributes,
                self.queue_url,
            )
        except ClientError as error:
            log_error("Couldn't publish message to queue %s.", self.queue_url)
            raise error
        else:
            return response

    def publish_fifo_queue(self):
        try:
            response = True
            # Todo: Need queue publishing backend code (Not Implemented yet)

            log_info(
                "Published message with attributes %s to queue %s.",
                self.attributes,
                self.queue_url,
            )
        except ClientError as error:
            log_error("Couldn't publish message to queue %s.", self.queue_url)
            raise error
        else:
            return response
