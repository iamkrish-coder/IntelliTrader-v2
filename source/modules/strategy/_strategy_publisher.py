# handlers/strategy
import boto3
import time

from source.constants.constants import *
from source.enumerations.enums import *
from source.utils.logging_utils import *
from source.utils.caching_utils import *
from source.aws.sqs.aws_sqs_manager import aws_sqs_publish
from source.aws.sns.aws_sns_manager import aws_sns_publish
from source.models.topics_model import TopicsModel


class StrategyPublisher:
    def __init__(self, modules, parameters, database, alerts, aws_service):
        self.modules = modules
        self.parameters = parameters
        self.database = database
        self.alerts = alerts
        self.aws_service = aws_service
        self.sns_client = boto3.client(SNS, region_name=REGION_NAME)
        self.sqs_client = boto3.client(SQS, region_name=REGION_NAME)

    def initialize(self):
        return self.publish()

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

    def generate_aws_sns_topic_name(self, strategy_id):

        # Create a mapping between strategy IDs and topic names
        strategy_id_enum = Strategy[f"ALGORITHM_{strategy_id}"]
        strategy_topic_mapping = {
            Strategy.ALGORITHM_1: Topics.TOPIC_1,
            Strategy.ALGORITHM_2: Topics.TOPIC_2,
            Strategy.ALGORITHM_3: Topics.TOPIC_3,
            Strategy.ALGORITHM_4: Topics.TOPIC_4,
            Strategy.ALGORITHM_5: Topics.TOPIC_5,
            Strategy.ALGORITHM_6: Topics.TOPIC_6,
        }

        if strategy_id_enum in strategy_topic_mapping:
            return strategy_topic_mapping[strategy_id_enum].value
        else:
            return None

    def generate_aws_sns_topic_arn(self, strategy_id):

        # ARN Template: arn:aws:sns:<region>:<account-id>:<topic-name>
        topic_name = self.generate_aws_sns_topic_name(strategy_id)

        enum_arn = AWS_SNS.ARN.value
        emum_aws = AWS_SNS.AWS.value
        emum_sns = AWS_SNS.SNS.value
        emum_region = AWS_SNS.REGION.value
        emum_account_id = AWS_SNS.ACCOUNT_ID.value
        emum_topic_name = topic_name

        arn_formatted = f"{enum_arn}:{emum_aws}:{emum_sns}:{emum_region}:{emum_account_id}:{emum_topic_name}.fifo"
        return arn_formatted, topic_name

    def get_aws_sqs_queue_name(self, strategy_id):
        # Create a mapping between strategy IDs and queue names
        strategy_id_enum = Strategy[f"algorithm_{strategy_id}"]
        strategy_queue_mapping = {
            Strategy.ALGORITHM_1: Queues.QUEUE_1,
            Strategy.ALGORITHM_2: Queues.QUEUE_2,
            Strategy.ALGORITHM_3: Queues.QUEUE_3,
            Strategy.ALGORITHM_4: Queues.QUEUE_4,
            Strategy.ALGORITHM_5: Queues.QUEUE_5,
            Strategy.ALGORITHM_6: Queues.QUEUE_6
        }

        if strategy_id_enum in strategy_queue_mapping:
            return strategy_queue_mapping[strategy_id_enum].value
        else:
            return None 

    def get_or_create_topic(self):

        log_info(f"Checking Existing SNS Topic...")
        dataset = {
                    "topic_arn": self.topic_arn,
                    "created_date": self.date_time_now,
                    "topic_name": self.topic_name,
                    "is_active": False,
                    "is_published": False,
                    "is_subscribed": False,
                    "is_deleted": False,
                }
        existing_topic_params = self.prepare_request_parameters(
            event=Events.QUERY.value,
            table=Tables.TABLE_TOPICS.value,
            model=TopicsModel,
            dataset=dataset,
            projection=["topic_arn", "topic_name"],
        )
        existing_topic = self.database_request(existing_topic_params)

        if existing_topic:
            cached_value = [dataset]
        else:
            log_info(f"Creating SNS Topic...")
            dataset = {
                "topic_arn": self.topic_arn,
                "created_date": self.date_time_now,
                "topic_name": self.topic_name,
                "is_active": False,
                "is_published": False,
                "is_subscribed": False,
                "is_deleted": False,
            }
            create_topic_params = self.prepare_request_parameters(
                event=Events.PUT.value,
                table=Tables.TABLE_TOPICS.value,
                model=TopicsModel,
                dataset=dataset,
            )
            self.database_request(create_topic_params)
            cached_value = [dataset]

        cached_key = f"{TABLE_TOPICS}_{self.topic_name}"
        set_cached_item(
            Cache_Type.DISK.value, 
            CACHE_TOPICS_DIR, 
            cached_key, 
            cached_value
        )

    def set_topic_published_status(self):

        log_info(f"Updating SNS Topic status...")                                
        dataset = {
            "topic_arn": self.topic_arn,
            "topic_name": self.topic_name,
            "is_active": True,
            "is_published": True,
        }
        update_topic_params = self.prepare_request_parameters(
            event=Events.UPDATE.value,
            table=Tables.TABLE_TOPICS.value,
            model=TopicsModel,
            dataset=dataset,
        )
        self.database_request(update_topic_params)

        cached_key = f"{TABLE_TOPICS}_{self.topic_name}_{IS_PUBLISHED}"
        cached_value = [dataset]
        set_cached_item(
            Cache_Type.DISK.value,
            CACHE_TOPICS_DIR,
            cached_key,
            cached_value,
        ) 

    def publish(self):
        ###############
        # SNS PUBLISH #
        ###############
        self.date_time_now = time.strftime("%Y-%m-%d %H:%M:%S")
        if self.aws_service == SNS:

            successfully_published = []
            strategy_id = self.parameters.get('strategy_id')
            if strategy_id is None:
                log_error("Strategy ID is missing from parameters.")
                return None    

            self.topic_arn, self.topic_name = self.generate_aws_sns_topic_arn(strategy_id)

            # Check existing disk cache
            cached_key = f"{TABLE_TOPICS}_{self.topic_name}"
            cached_value = get_cached_item(
                Cache_Type.DISK.value, 
                CACHE_TOPICS_DIR, 
                cached_key
            )

            if not cached_value:
                self.get_or_create_topic()  
                
            for alert in self.alerts:
                exchange, symbol, token = alert.split(",")
                message = f"{exchange.strip()}, {symbol.strip()}, {token.strip()}"
                subject = "Stock Alert"

                try:
                    response = aws_sns_publish(self.sns_client, self.topic_arn, message, subject)
                    if "MessageId" in response:
                        successfully_published.append(message)
                    else:
                        log_error("Failed to get Message ID in response.")
                except Exception as e:
                    log_error(f"Error publishing message to SNS: {str(e)}")

                time.sleep(1)

                if len(successfully_published) == len(self.alerts):
                    config = self.database.table_configuration.get(Tables.TABLE_TOPICS.value)
                    if config:
                        cached_key = f"{TABLE_TOPICS}_{self.topic_name}_{IS_PUBLISHED}"
                        cached_value = get_cached_item(
                            Cache_Type.DISK.value, 
                            CACHE_TOPICS_DIR, 
                            cached_key
                        )

                        if cached_value is None:
                            self.set_topic_published_status()

                    log_info("Alerts Published ...COMPLETE!")
                    break

        ###############
        # SQS PUBLISH #
        ###############

        if self.aws_service == SQS:
            successfully_published = []
            strategy_id = self.parameters.get("strategy_id")

            if strategy_id is None:
                log_error("Strategy ID is missing from parameters.")
                return None

            self.strategy_queue = self.get_aws_sqs_queue_name(strategy_id)
            if self.strategy_queue is None:
                log_error(f"Queue name not found for Strategy {strategy_id}.")
                return None

            url = (
                f"{AWS_SQS.URL.value}/{AWS_SQS.ACCOUNT_ID.value}/{self.strategy_queue}"
            )

            for alert in self.alerts:
                exchange, symbol, token = alert.split(", ")
                message = f"{exchange.strip()}, {symbol.strip()}, {token.strip()}"

                try:
                    response = aws_sqs_publish(self.client, message, url)

                    if "MessageId" in response:
                        successfully_published.append(message)
                    else:
                        log_error("Failed to get Message ID in response.")
                except Exception as e:
                    log_error(f"Error publishing message to SQS: {str(e)}")

                time.sleep(1)
                if len(successfully_published) == len(self.alerts):
                    log_info("Alerts Published ...COMPLETE!")
                    break
