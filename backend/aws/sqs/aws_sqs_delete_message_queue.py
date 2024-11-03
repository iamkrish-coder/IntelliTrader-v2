import boto3

from botocore.exceptions import ClientError
from .BaseSqsManager import BaseSqsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class DeleteMessageQueue(BaseSqsManager):
    """Encapsulates Amazon SQS queue."""

    def __init__(self, queue_url, receipt_handle):
        """
        :param sqs_client_resource: A Boto3 Amazon SQS client resource.
        """
        self.sqs_client = boto3.client(SQS, region_name=REGION_NAME)
        self.queue_url = queue_url
        self.receipt_handle = receipt_handle

    def execute(self):
        try:
            response = self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=self.receipt_handle
            )
            log_info("Deleted message: %s", response.get("message_id"))
        except ClientError as error:
            log_error("Couldn't delete message: %s", response.get("message_id"))
            raise error
        else:
            return response
