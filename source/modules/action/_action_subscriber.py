# handlers/actions

import time
import boto3

from ...constants.const import *
from ...enumerations.enums import *
from ...utils.logging_utils import *
from ...utils.caching_utils import *
from ...aws.sqs.aws_sqs_manager import SQSManager
from ...aws.sns.aws_sns_manager import SNSManager
from .BaseAction import BaseAction


class ActionSubscriber(BaseAction):
    def __init__(self, connection, modules, parameters, database, subscriber):
        super().__init__(connection, modules)
        self.strategy_queue = None
        self.connection = connection
        self.modules = modules
        self.parameters = parameters
        self.database = database
        self.subscriber = subscriber
        self.object_sns_manager = SNSManager()
        self.object_sqs_manager = SQSManager()
        self.alerts = None
        self.queue_type = self.parameters.get('runtime_params.queue_type')
        self.topic_type = self.parameters.get('runtime_params.topic_type')
        self.strategy_id = self.parameters.get('strategy_params.strategy_id')

    def initialize(self):
        return self.subscribe()

    def prepare_request_parameters(self, event, table, model, dataset, projection=[], filters={}):

        attributes = None
        config = self.database.table_configuration[table]
        if model:
            attributes = model(**dataset).convert_table_rows_to_dict(config)
        return {
            "event": event,
            "table": table,
            "config": config,
            "data": {
                "attributes": attributes,
                "projection": projection,
                "filters": filters,
            }
        }

    def database_request(self, request):
        log_info(f"Requesting AWS DynamoDB...")
        return self.database.manage_table_records(request)

    def get_topics_for_subscription(self):

        dataset = None
        active_topic_params = self.prepare_request_parameters(
            event=Events.SCAN.value,
            table=Tables.TABLE_TOPICS.value,
            model=None,
            dataset=dataset,
            projection=["topic_arn"],
            filters={
                "is_subscribed": { "eq": False },
                "is_active": {'eq': True}
            }
        )
        return self.database_request(active_topic_params)

    def subscribe(self):
        ###################
        # SNS SUBSCRIBE #
        ###################
        if self.subscriber == SNS:
            successfully_subscribed = []
            if self.strategy_id is None:
                log_error("Strategy ID is missing from parameters.")
                return None

            queue_arn, queue_name, queue_url = self.generate_aws_sqs_queue_details(self.strategy_id, self.queue_type)
            topic_arn, topic_name = self.generate_aws_sns_topic_details(self.strategy_id, self.topic_type)

            # Subscribe the SQS queue to the SNS topic
            try:
                arguments = {
                    "queue_url": queue_url,
                    "attribute_names": ['All'],
                    "max_number_of_messages": 5,
                    "message_attribute_names": ['All'],
                    "message_system_attribute_names": ['All'],
                    "visibility_timeout": 60,
                    "wait_time_seconds": 10
                }
                subscribe_topic = self.object_sqs_manager.get_action("subscribe_queue", **arguments)
                response = subscribe_topic.execute()
            except Exception as error:
                log_error(f"Error receiving Messages: {str(error)}")
                return False
            log_info(f"Received: {queue_name}: {response.get('ResponseMetadata', {}).get('RequestId')}")

            if response is None:
                log_info("No messages available in the subscribed queue.")
                return None
            else:
                return response

        #################
        # SQS SUBSCRIBE #
        #################
        if self.subscriber == SQS:
            # Todo: Need queue sub subscription and receiving messages source code (Not Implemented yet)
            log_warn(f"SQS Subscriber {self.subscriber} is NOT implemented yet.")

