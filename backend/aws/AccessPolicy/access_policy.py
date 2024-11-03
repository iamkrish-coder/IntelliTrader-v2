import os
import json
import boto3

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.modules.helper.helper_module import Helper


class AccessPolicy:

    def __init__(self, service):
        self.service = service
        self.account = self.get_aws_account_id()

    def get_policy(self):
        # Implement logic to build the complete access policy based on service and statement
        # This can involve string formatting or JSON construction
        statement = self.get_policy_statement()
        policy = {
            "Version": "2012-10-17",
            "Statement": statement
        }
        return policy

    def get_aws_account_id(self):
        sts_client = boto3.client('sts')
        response = sts_client.get_caller_identity()
        account_id = response['Account']
        return account_id

    def get_policy_statement(self):
        """
          Reads and returns the service access policy statement found in JSON files within the same folder.

          Returns:
              dict: The access policy statement as a dictionary (if found), otherwise None.
          """
        # Get the current directory path
        # Check if the service-specific file exists
        filename = f"{self.service}.json"
        file_path = os.path.join(OUTPUT_PATH, filename)

        if os.path.isfile(file_path):
            # Open the file and attempt to read the policy statement
            try:
                with open(file_path, "r") as f:
                    policy_statement = json.load(f)
                    return policy_statement
            except (FileNotFoundError, json.JSONDecodeError):
                # Handle potential errors (file not found or invalid JSON)
                print(f"Error reading policy statement from {filename}")
                pass

        # No valid policy statement found
        log_info(f"Policy statement not found for service: {self.service}")
        return None

    def set_policy_statement(self, aws_topic_resource, aws_queue_resource=None):
        statement = None
        match self.service:
            case "sns":
                statement = self.sns_service_statement(aws_topic_resource)
            case "sqs":
                statement = self.sqs_service_statement(aws_queue_resource, aws_topic_resource)
            case _:
                log_warn("The indicator option provided is not valid")

        Helper().write_text_output(f"{self.service}.json", statement)
        log_info(f"Policy statements generated for service: {self.service}")

    def sns_service_statement(self, topic_arn):
        statement = [
            {
                "Sid": "__default_statement_ID",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": [
                    "SNS:GetTopicAttributes",
                    "SNS:SetTopicAttributes",
                    "SNS:AddPermission",
                    "SNS:RemovePermission",
                    "SNS:DeleteTopic",
                    "SNS:Subscribe",
                    "SNS:ListSubscriptionsByTopic",
                    "SNS:Publish"
                ],
                "Resource": topic_arn,
                "Condition": {
                    "StringEquals": {
                        "aws:PrincipalAccount": self.account
                    }
                }
            }
        ]
        return statement

    def sqs_service_statement(self, queue_arn, topic_arn=None):
        statement = [
            {
                "Sid": "__owner_statement",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "265153260161"
                },
                "Action": [
                    "SQS:*"
                ],
                "Resource": queue_arn
            },
            {
                "Sid": "topic-subscription-arn:aws:sns:ap-south-1:265153260161:T-STR-001.fifo",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": "SQS:SendMessage",
                "Resource": queue_arn,
                "Condition": {
                    "ArnLike": {
                        "aws:SourceArn": topic_arn
                    }
                }
            }
        ]
        return statement