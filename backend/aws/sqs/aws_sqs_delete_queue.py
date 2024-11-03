import boto3

from botocore.exceptions import ClientError
from .BaseSqsManager import BaseSqsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class DeleteQueue(BaseSqsManager):
    """Encapsulates Amazon SQS queue."""

    def __init__(self, queue_url):
        """
        :param sqs_client_resource: A Boto3 Amazon SQS client resource.
        """
        self.sqs_client = boto3.client(SQS, region_name=REGION_NAME)
        self.queue_url = queue_url

    def execute(self):
        """
        Removes an SQS queue. When run against an AWS account, it can take up to
        60 seconds before the queue is actually deleted.

        :param queue: The queue to delete.
        :return: None
        """
        try:
            response = self.sqs_client.delete_queue(
                QueueUrl=self.queue_url
            )
            log_info("Deleted queue with URL=%s.", self.queue_url)
        except ClientError as error:
            log_error("Couldn't delete queue with URL=%s!", self.queue_url)
            raise error
        else:
            return response
