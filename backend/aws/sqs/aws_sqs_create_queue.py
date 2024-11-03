import json

import boto3

from botocore.exceptions import ClientError
from .BaseSqsManager import BaseSqsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class CreateQueue(BaseSqsManager):
    """Encapsulates Amazon SQS queue."""

    def __init__(self, mode, queue_name, access_policy=None, fifo_queue=None, content_based_deduplication=None, delay_seconds=None, maximum_message_size=None, receive_message_wait_time_seconds=None, message_retention_period=None, visibility_timeout=None):
        """
            Initializes the SQS queue object.

            :param mode (str): The mode of the queue (e.g., 'standard' or 'fifo').
            :param queue_name (str): The name of the SQS queue.
            :param access_policy (dict, optional): The access policy for the queue. Defaults to None.
            :param fifo_queue (bool, optional): Whether the queue is a FIFO queue. Defaults to None.
            :param content_based_deduplication (bool, optional): Whether content-based deduplication is enabled for the queue. Defaults to None.
            :param delay_seconds (int, optional): The number of seconds messages are delayed before they become available for consumption. Defaults to None.
            :param maximum_message_size (int, optional): The maximum allowed size (in bytes) of a message in the queue. Defaults to None.
            :param receive_message_wait_time_seconds (int, optional): The wait time for receiving messages from the queue (in seconds). Defaults to None.
            :param message_retention_period (int, optional): The number of seconds messages are retained after they are delivered. Defaults to None.
            :param visibility_timeout (int, optional): The visibility timeout for messages (in seconds). Defaults to None.
        """
        self.sqs_client = boto3.client(SQS, region_name=REGION_NAME)
        self.mode = mode
        self.queue_name = queue_name
        self.access_policy = access_policy
        self.fifo_queue = fifo_queue
        self.content_based_deduplication = content_based_deduplication
        self.delay_seconds = delay_seconds
        self.maximum_message_size = maximum_message_size
        self.receive_message_wait_time_seconds = receive_message_wait_time_seconds
        self.message_retention_period = message_retention_period
        self.visibility_timeout = visibility_timeout

    def execute(self):
        if self.mode == STANDARD:
            return self.create_standard_queue()
        elif self.mode == FIFO:
            return self.create_fifo_queue()

    def create_standard_queue(self):
        try:
            # Define queue attributes dictionary
            queue_attributes = {
                'DelaySeconds': self.delay_seconds,
                'MaximumMessageSize': self.maximum_message_size,
                'ReceiveMessageWaitTimeSeconds': self.receive_message_wait_time_seconds,
                'MessageRetentionPeriod': self.message_retention_period,
                'VisibilityTimeout': self.visibility_timeout,
                'Policy': json.dumps(self.access_policy)
            }

            queue_attributes = {key: value for key, value in queue_attributes.items() if value is not None}

            response = self.sqs_client.create_queue(
                QueueName=self.queue_name,
                Attributes=queue_attributes
            )
            log_info("Created queue '%s' with URL=%s", self.queue_name, response.get("QueueUrl"))
        except ClientError as error:
            log_error("Couldn't create queue %s.", self.queue_name)
            raise error
        else:
            return response

    def create_fifo_queue(self):
        """
        Create a FIFO queue.
        queue names must be made up of only uppercase and lowercase ASCII letters,
        numbers, underscores, and hyphens, and must be between 1 and 256 characters long.
        For a FIFO queue, the name must end with the .fifo suffix.

        :return: The new queue.
        """
        try:
            # Define queue attributes dictionary
            queue_attributes = {
                'DelaySeconds': self.delay_seconds,
                'FifoQueue': self.fifo_queue,
                'ContentBasedDeduplication': self.content_based_deduplication,
                'MaximumMessageSize': self.maximum_message_size,
                'ReceiveMessageWaitTimeSeconds': self.receive_message_wait_time_seconds,
                'MessageRetentionPeriod': self.message_retention_period,
                'VisibilityTimeout': self.visibility_timeout,
                'Policy': json.dumps(self.access_policy)
            }

            queue_attributes = {key: value for key, value in queue_attributes.items() if value is not None}

            response = self.sqs_client.create_queue(
                QueueName=self.queue_name,
                Attributes=queue_attributes
            )
            log_info("Created FIFO queue '%s' with URL=%s", self.queue_name, response.get("QueueUrl"))
        except ClientError as error:
            log_error("Couldn't create queue %s.", self.queue_name)
            raise error
        else:
            return response