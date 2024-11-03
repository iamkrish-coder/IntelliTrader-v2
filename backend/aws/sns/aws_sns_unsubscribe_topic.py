import boto3

from botocore.exceptions import ClientError
from .BaseSnsManager import BaseSnsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class UnsubscribeTopic(BaseSnsManager):
    """Encapsulates Amazon SNS topic."""

    def __init__(self, subscription_arn=None):
        """
        :param sns_client_resource: A Boto3 Amazon SNS client resource.
        """
        self.sns_client = boto3.client(SNS, region_name=REGION_NAME)
        self.subscription_arn = subscription_arn

    def execute(self):
        """
        Unsubscribes and deletes a subscription.
        """
        try:
            if self.subscription_arn is not None and self.subscription_arn != "":
                self.sns_client.unsubscribe(SubscriptionArn=self.subscription_arn)
                log_info("Deleted subscription %s.", self.subscription_arn)
        except ClientError as error:
            log_error("Couldn't delete subscription %s.", self.subscription_arn)
            raise error
