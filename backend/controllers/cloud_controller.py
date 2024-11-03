"""
Cloud - AWS Controller
"""
import time

from backend.utils.logging_utils import *
from backend.aws.AccessPolicy.access_policy import AccessPolicy
from backend.aws.sns.aws_sns_manager import SNSManager
from backend.aws.sqs.aws_sqs_manager import SQSManager
from backend.models.strategies_model import StrategiesModel
from backend.models.topics_model import TopicsModel
from backend.models.queues_model import QueuesModel
from backend.controllers.database_controller import DatabaseController
from backend.controllers.BaseController import BaseController


class CloudController(BaseController):

    def __init__(self, _base_):
        super().__init__(_base_.connection, _base_.modules, _base_.configuration, _base_.database)
        self.object_sns_manager = SNSManager()
        self.object_sqs_manager = SQSManager()
        self.topic_mode = self.configuration.get("topic_type")
        self.queue_mode = self.configuration.get("queue_type")
        self.strategy_list = []
        self.selected_strategy = None

    ###########################################
    # Initialize Strategy Module
    ###########################################

    def initialize(self):
        # Manage strategies
        if not self.manage_strategies():
            return False

        # Manage access policies
        if not self.manage_access_policies():
            return False

        # Manage topics
        if not self.manage_topics():
            return False

        # Manage queues
        if not self.manage_queues():
            return False

        # Manage subscriptions
        if not self.manage_subscriptions():
            return False

        # All successful, return True
        return True

    def get_strategy_list(self):
        dataset = None
        list_strategies = self.prepare_request_parameters(
            event=Events.SCAN.value,
            table=Tables.TABLE_STRATEGIES.value,
            model=None,
            dataset=dataset,
            projection=["strategy_id", "strategy_name"],
        )
        self.strategy_list = self.database.database_request(list_strategies)

    def manage_strategies(self):
        """
        Pre-Requisite Strategy Operations
        """
        try:
            # Get strategy list from database
            saved_strategy_list = []
            self.get_strategy_list()
            if self.strategy_list is not None:
                for strategy in self.strategy_list:
                    saved_strategy_list.append(strategy.get("strategy_id"))

            # Check if Strategy already exists in database if not add strategy to database
            for filename in os.listdir(ALGORITHM_PATH):
                strategy_id, strategy_name, strategy_type, strategy_description = self.generate_strategy_details(filename)
                if strategy_id in saved_strategy_list:
                    continue

                # strategy_id = self.generate_table_uid(TABLE_STRATEGIES)
                dataset = {
                    "strategy_id": strategy_id,
                    "strategy_name": strategy_name,
                    "strategy_type": strategy_type,
                    "strategy_description": strategy_description,
                    "created_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                save_strategies = self.prepare_request_parameters(
                    event=Events.PUT.value,
                    table=Tables.TABLE_STRATEGIES.value,
                    model=StrategiesModel,
                    dataset=dataset
                )
                self.database.database_request(save_strategies)

            # Select strategy for further use
            strategy = self.configuration.get("strategy")
            self.selected_strategy = self.configuration.get(f"strategy_{strategy}_params").get("strategy_id")
            return True
        except Exception as error:
            log_error(f"Error setting up strategies: {str(error)}")
            return False

    def manage_access_policies(self):
        return True

    def manage_topics(self):
        """
        Pre-Requisite Topic Operations
        """
        # List Topics
        try:
            arguments = {}
            list_topics = self.object_sns_manager.get_action("list_topics", **arguments)
            response = list_topics.execute()
            topics_list = response.get("Topics")

            # Get strategies
            if self.strategy_list is None:
                self.get_strategy_list()

            # Check strategies
            if self.strategy_list is None:
                log_info(f"No Strategy Topics to manage.")
                return False

            # Check Topics
            saved_topics_list = []
            if topics_list is not None and topics_list != []:
                for topics in topics_list:
                    saved_topics_list.append(topics.get("TopicArn"))

            # Create Topics
            for strategy in self.strategy_list:
                strategy_id = strategy.get("strategy_id")
                if strategy_id == '000':
                    continue

                topic_arn, topic_name = self.generate_aws_sns_topic_details(strategy_id, self.topic_mode)

                if topic_arn in saved_topics_list:
                    log_info(f"Skipping topic creation for Strategy {strategy_id}")
                    continue
                else:
                    # Create Topic in AWS SNS
                    try:
                        """ Access Policy """
                        object_access_policy = AccessPolicy(SNS)
                        object_access_policy.set_policy_statement(aws_topic_resource=topic_arn)
                        access_policy = object_access_policy.get_policy()

                        arguments = {
                            "mode": self.topic_mode,
                            "topic_name": topic_name,
                            "display_name": str("Stock-Alerts-" + strategy_id),
                            "fifo_topic": str(True),
                            "content_based_deduplication": str(False),
                            "access_policy": access_policy
                        }
                        create_topic = self.object_sns_manager.get_action("create_topic", **arguments)
                        create_topic.execute()
                    except Exception as error:
                        log_error(f"Error creating Topic: {str(error)}")
                        return False

                    # Add entry to AWS DynamoDB
                    topic_id = self.generate_table_uid(TABLE_TOPICS)
                    dataset = {
                        "topic_id": topic_id,
                        "topic_arn": topic_arn,
                        "topic_name": topic_name,
                        "strategy_id": strategy_id,
                        "created_date": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    save_topics = self.prepare_request_parameters(
                        event=Events.PUT.value,
                        table=Tables.TABLE_TOPICS.value,
                        model=TopicsModel,
                        dataset=dataset
                    )
                    self.database.database_request(save_topics)
            return True
        except Exception as error:
            log_error(f"Error setting up topics: {str(error)}")
            return False

    def manage_queues(self):
        """
        Pre-Requisite Queue Operations
        """
        # List Queues
        try:
            arguments = {}
            list_queues = self.object_sqs_manager.get_action("list_queues", **arguments)
            response = list_queues.execute()
            queues_list = response.get("QueueUrls")

            # Get strategies
            if self.strategy_list is None:
                self.get_strategy_list()

            # Check strategies
            if self.strategy_list is None:
                log_info(f"No Strategy Queues to manage.")
                return

            # Check Queues
            saved_queues_list = []
            if queues_list is not None and queues_list != []:
                for queues in queues_list:
                    saved_queues_list.append(queues)

            # Create Queues
            for strategy in self.strategy_list:
                strategy_id = strategy.get("strategy_id")
                if strategy_id == '000':
                    continue

                queue_arn, queue_name, queue_url = self.generate_aws_sqs_queue_details(strategy_id, self.queue_mode)
                topic_arn, topic_name = self.generate_aws_sns_topic_details(strategy_id, self.topic_mode)

                if queue_url in saved_queues_list:
                    log_info(f"Skipping Queue creation for Strategy {strategy_id}")
                    continue

                # Create Queue in AWS SQS
                try:
                    """ Access Policy """
                    object_access_policy = AccessPolicy(SQS)
                    object_access_policy.set_policy_statement(aws_queue_resource=queue_arn, aws_topic_resource=topic_arn)
                    access_policy = object_access_policy.get_policy()

                    arguments = {
                        "mode": self.queue_mode,
                        "queue_name": queue_name,
                        "delay_seconds": str(0),
                        "maximum_message_size": str(4096),
                        "receive_message_wait_time_seconds": str(10),
                        "message_retention_period": str(300),
                        "visibility_timeout": str(300),
                        "fifo_queue": str(True),
                        "content_based_deduplication": str(True),
                        "access_policy": access_policy
                    }
                    create_queue = self.object_sqs_manager.get_action("create_queue", **arguments)
                    create_queue.execute()
                except Exception as error:
                    log_error(f"Error creating Queue: {str(error)}")
                    return False

                # Add entry to AWS DynamoDB
                queue_id = self.generate_table_uid(TABLE_QUEUES)
                dataset = {
                    "queue_id": queue_id,
                    "queue_arn": queue_arn,
                    "queue_name": queue_name,
                    "queue_url": queue_url,
                    "strategy_id": strategy_id,
                    "created_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                save_queues = self.prepare_request_parameters(
                    event=Events.PUT.value,
                    table=Tables.TABLE_QUEUES.value,
                    model=QueuesModel,
                    dataset=dataset
                )
                self.database.database_request(save_queues)
            return True
        except Exception as error:
            log_error(f"Error setting up queues: {str(error)}")
            return False

    def manage_subscriptions(self):
        """
        Pre-Requisite Subscription Operations
        """
        if self.strategy_list is None:
            log_info(f"No Strategy Subscriptions to manage.")
            return False

        for strategy in self.strategy_list:
            strategy_id = strategy.get("strategy_id")
            if strategy_id == '000':
                continue

            topic_arn, topic_name = self.generate_aws_sns_topic_details(strategy_id, self.topic_mode)
            queue_arn, queue_name, queue_url = self.generate_aws_sqs_queue_details(strategy_id, self.queue_mode)

            try:
                # List Subscriptions
                arguments = {"topic_arn": topic_arn}
                list_subscriptions = self.object_sns_manager.get_action("list_subscriptions", **arguments)
                subscriptions = list_subscriptions.execute()
                subscription_list = subscriptions.get("Subscriptions")

                arguments = {}
                list_queues = self.object_sqs_manager.get_action("list_queues", **arguments)
                response = list_queues.execute()
                queues_list = response.get("QueueUrls")

                if queues_list is not None and queues_list != []:
                    # Todo: This needs to define endpoint subscription type to create the multiple types of subscription
                    # Todo: Currently only handles SNS -> SQS
                    if subscription_list is not None and subscription_list != []:
                        for subscription in subscription_list:
                            if subscription.get("Endpoint") != queue_arn:
                                self.create_save_subscriptions(topic_arn, queue_arn)
                                log_info(f"Subscription created for {topic_name}!")
                            else:
                                log_info(f"Skipping Subscription creation for {topic_name}, Topic already Subscribed!")
                    else:
                        if self.create_save_subscriptions(topic_arn, queue_arn):
                            log_info(f"Subscription created for {topic_name}!")
                        else:
                            return False
            except Exception as error:
                log_error(f"Error setting up subscriptions: {str(error)}")
                return False
        return True

    def create_save_subscriptions(self, topic_arn, queue_arn):
        # Create Subscription in AWS SNS
        if topic_arn is not None and queue_arn is not None:
            try:
                arguments = {
                    "topic_arn": topic_arn,
                    "protocol": SQS,
                    "endpoint": queue_arn
                }
                subscribe_topic = self.object_sns_manager.get_action("subscribe_topic", **arguments)
                subscribe_topic.execute()
            except Exception as error:
                log_error(f"Error creating Subscriptions: {str(error)}")
                return False

            # Add entry to AWS DynamoDB
            topic_id = self.generate_table_uid(TABLE_TOPICS)
            dataset = {
                "topic_id": topic_id,
                "topic_arn": topic_arn,
                "modified_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "is_subscribed": True,
                "is_active": True
            }
            update_topics = self.prepare_request_parameters(
                event=Events.UPDATE.value,
                table=Tables.TABLE_TOPICS.value,
                model=TopicsModel,
                dataset=dataset
            )
            self.database.database_request(update_topics)

    def delete_subscriptions(self):
        try:
            list_topics = self.object_sns_manager.get_action("list_topics", **{})
            topics_list = (list_topics.execute()).get("Topics")
            if topics_list is not None:
                for topics in topics_list:
                    topic_arn = topics.get("TopicArn")
                    arguments = {"topic_arn": topic_arn}
                    list_subscriptions = self.object_sns_manager.get_action("list_subscriptions", **arguments)
                    subscriptions = list_subscriptions.execute()
                    subscription_list = subscriptions.get("Subscriptions")
                    if subscription_list is not None:
                        for subscription in subscription_list:
                            subscription_arn = subscription.get("SubscriptionArn")
                            arguments = {"subscription_arn": subscription_arn}
                            unsubscribe_topic = self.object_sns_manager.get_action("unsubscribe_topic", **arguments)
                            unsubscribe_topic.execute()
                            # TODO : Update DB is_subscribed = False and is_active = False
            else:
                log_info(f"No subscriptions to delete.")
            return True
        except Exception as error:
            log_error(f"Error deleting Subscriptions: {str(error)}")
            return False

    def delete_topics(self):
        try:
            list_topics = self.object_sns_manager.get_action("list_topics", **{})
            topics_list = (list_topics.execute()).get("Topics")
            if topics_list is not None:
                for topics in topics_list:
                    topic_arn = topics.get("TopicArn")
                    arguments = {"topic_arn": topic_arn}
                    delete_topic = self.object_sns_manager.get_action("delete_topic", **arguments)
                    delete_topic.execute()
            else:
                log_info("No topics to delete.")
            return True
        except Exception as error:
            log_error(f"Error deleting Topics: {str(error)}")
            return False

    def delete_queues(self):
        try:
            list_queues = self.object_sqs_manager.get_action("list_queues", **{})
            queues_list = (list_queues.execute()).get("QueueUrls")
            if queues_list is not None:
                for queues in queues_list:
                    queue_url = queues
                    arguments = {"queue_url": queue_url}
                    delete_queue = self.object_sqs_manager.get_action("delete_queue", **arguments)
                    delete_queue.execute()
            else:
                log_info("No queues to delete.")
            return True
        except Exception as error:
            log_error(f"Error deleting Queues: {str(error)}")
            return False
