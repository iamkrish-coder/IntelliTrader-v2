import boto3

from botocore.exceptions import ClientError
from .BaseSnsManager import BaseSnsManager
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *


class SubscribeTopic(BaseSnsManager):
    """Encapsulates Amazon SNS topic."""

    def __init__(self, topic_arn, protocol, endpoint, delivery_policy=None, filter_policy=None, redrive_policy=None):
        """
            Initializes the SNS subscription object.

            :param topic_arn (str): The ARN of the SNS topic to subscribe to.
            :param protocol (str): The protocol to use for delivering messages (e.g., 'http', 'https', 'sqs').
            :param endpoint (str): The endpoint to which messages are delivered.
                                   - For 'http' or 'https' protocols, it's the URL of the endpoint.
                                   - For 'sqs' protocol, it's the ARN of the SQS queue.
            :param delivery_policy (dict, optional): The message delivery policy for the subscription. Defaults to None.
            :param filter_policy (str, optional): The message filtering policy for the subscription. Defaults to None.
            :param redrive_policy (dict, optional): The redrive policy for the subscription. Defaults to None.
        """
        self.sns_client = boto3.client(SNS, region_name=REGION_NAME)
        self.topic_arn = topic_arn
        self.protocol = protocol
        self.endpoint = endpoint
        self.delivery_policy = delivery_policy
        self.filter_policy = filter_policy
        self.redrive_policy = redrive_policy

    def execute(self):
        try:
            # Define queue attributes dictionary
            subscriber_attributes = {
                'DeliveryPolicy': self.delivery_policy,
                'FilterPolicy': self.filter_policy,
                'RedrivePolicy': self.redrive_policy
            }
            subscriber_attributes = {key: value for key, value in subscriber_attributes.items() if value is not None}

            response = self.sns_client.subscribe(
                TopicArn=self.topic_arn,
                Protocol=self.protocol,
                Endpoint=self.endpoint,
                Attributes=subscriber_attributes,
                ReturnSubscriptionArn=True
            )
            log_info("Subscribed %s %s to topic %s.", self.protocol, self.endpoint, self.topic_arn)
        except ClientError as error:
            log_error(
                "Couldn't subscribe %s %s to topic %s.", self.protocol, self.endpoint, self.topic_arn)
            raise error
        else:
            return response