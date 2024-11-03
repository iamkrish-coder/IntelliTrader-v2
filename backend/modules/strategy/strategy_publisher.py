# handlers/strategy
import time
import uuid

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *
from ...aws.sns.aws_sns_manager import SNSManager
from ...aws.sqs.aws_sqs_manager import SQSManager
from ...controllers.BaseController import BaseController
from ...models.topics_model import TopicsModel
from .BaseStrategy import BaseStrategy


class StrategyPublisher(BaseController, BaseStrategy):
    def __init__(self, _base_, parameters, alerts, publisher):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.parameters = parameters
        self.alerts = alerts
        self.publisher = publisher
        self.object_sns_manager = SNSManager()
        self.object_sqs_manager = SQSManager()
        self.strategy_id = self.parameters.get("strategy_params.strategy_id")
        self.topic_mode = self.parameters.get("runtime_params.topic_type")
        self.queue_mode = self.parameters.get("runtime_params.queue_type")
        self.strategy_queue = None
        self.date_time_now = None
        self.client = None

    def initialize(self):
        return self.publish()

    # def set_topic_published_status(self):
    #
    #     log_info(f"Updating SNS Topic status...")
    #     dataset = {
    #         "topic_arn": topic_arn,
    #         "topic_name": topic_name,
    #         "is_active": True,
    #         "is_published": True,
    #     }
    #     update_topic_params = self.prepare_request_parameters(
    #         event=Events.UPDATE.value,
    #         table=Tables.TABLE_TOPICS.value,
    #         model=TopicsModel,
    #         dataset=dataset,
    #     )
    #     self.database_request(update_topic_params)
    #
    #     cached_key = f"{TABLE_TOPICS}_{topic_name}_{IS_PUBLISHED}"
    #     cached_value = [dataset]
    #     set_cached_item(
    #         Cache_Type.DISK.value,
    #         CACHE_TOPICS_DIR,
    #         cached_key,
    #         cached_value,
    #     )

    def publish(self):
        ###############
        # SNS PUBLISH #
        ###############
        if self.publisher == SNS:
            successfully_published = []
            if self.strategy_id is None:
                log_error("Strategy ID is missing from parameters.")
                return None

            """ Build Parameters """
            topic_arn, topic_name = self.generate_aws_sns_topic_details(
                self.strategy_id, self.topic_mode
            )
            group_id = self.generate_group_id(self.strategy_id)

            for alert in self.alerts:
                exchange, symbol, token = alert.split(",")
                message = f"{exchange.strip()}, {symbol.strip()}, {token.strip()}"
                subject = "IntelliTrader - Stock Alert"
                deduplication_id = uuid.uuid4()

                try:
                    # Publish to SNS
                    arguments = {
                        "mode": self.topic_mode,
                        "topic_name": topic_name,
                        "topic_arn": topic_arn,
                        "message": message,
                        "subject": subject,
                        "deduplication_id": deduplication_id,
                        "group_id": group_id,
                    }
                    publish_topic = self.object_sns_manager.get_action(
                        "publish_topic", **arguments
                    )
                    response = publish_topic.execute()

                    if "MessageId" in response:
                        successfully_published.append(message)
                    else:
                        log_error("Failed to get Message ID in response.")

                    time.sleep(1)
                except Exception as error:
                    log_error(f"Error publishing message to SNS: {str(error)}")

                if len(successfully_published) == len(self.alerts):
                    log_info("Alerts Published ...COMPLETE!")
                    break

        ###############
        # SQS PUBLISH #
        ###############
        if self.publisher == SQS:
            # Todo: Need queue publishing and sending messages backend code (Not Implemented yet)
            log_warn(f"SQS Publisher {self.publisher} is NOT implemented yet.")
