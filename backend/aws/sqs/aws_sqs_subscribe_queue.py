import boto3

from botocore.exceptions import ClientError
from .BaseSqsManager import BaseSqsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class SubscribeQueue(BaseSqsManager):
    """Encapsulates Amazon SQS queue."""

    def __init__(self, queue_url, attribute_names=None, max_number_of_messages=None, message_attribute_names=None,
                 message_system_attribute_names=None, receive_request_attempt_id=None, visibility_timeout=None,
                 wait_time_seconds=None):
        """
        :param sqs_client_resource: A Boto3 Amazon SQS client resource.
        """
        self.sqs_client = boto3.client('sqs', region_name=REGION_NAME)
        self.queue_url = queue_url
        self.attribute_names = attribute_names
        self.max_number_of_messages = max_number_of_messages
        self.message_attribute_names = message_attribute_names
        self.message_system_attribute_names = message_system_attribute_names
        self.receive_request_attempt_id = receive_request_attempt_id
        self.visibility_timeout = visibility_timeout
        self.wait_time_seconds = wait_time_seconds

    def execute(self):
        """
        Receive a batch of messages in a single request from an SQS queue.
        """
        try:
            response = self.sqs_client.receive_message(
                QueueUrl=self.queue_url,
                AttributeNames=self.attribute_names,
                MaxNumberOfMessages=self.max_number_of_messages,
                MessageAttributeNames=self.message_attribute_names,
                MessageSystemAttributeNames=self.message_system_attribute_names,
                # ReceiveRequestAttemptId=self.receive_request_attempt_id,
                VisibilityTimeout=self.visibility_timeout,
                WaitTimeSeconds=self.wait_time_seconds
            )
            if response and 'Messages' in response:
                messages = response.get('Messages')
                for message in messages:
                    log_info("Received message: %s: %s", message.get('MessageId'), message.get('Body'))
            else:
                log_info("Received no messages")
                return None
        except ClientError as error:
            log_error("Couldn't receive message from queue: %s", response.get("QueueName"))
            raise error
        else:
            return response
