import boto3

from botocore.exceptions import ClientError
from .BaseSqsManager import BaseSqsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class ListQueues(BaseSqsManager):
    """Encapsulates Amazon SQS queue."""

    def __init__(self, prefix=None):
        """
        :param sqs_client_resource: A Boto3 Amazon SQS client resource.
        """
        self.sqs_client = boto3.client(SQS, region_name=REGION_NAME)
        self.prefix = prefix

    def execute(self):
        """
        Gets a list of SQS queues. When a prefix is specified, only queues with names
        that start with the prefix are returned.

        :param prefix: The prefix used to restrict the list of returned queues.
        :return: A list of Queue objects.
        """
        try:
            if self.prefix:
                response = self.sqs_client.list_queues(
                    QueueNamePrefix=self.prefix
                )
            else:
                response = self.sqs_client.list_queues()
        except ClientError as error:
            log_warn("Couldn't get queues.")
            raise error
        else:
            return response
