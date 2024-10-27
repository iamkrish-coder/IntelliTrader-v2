# aws_dynamodb.py

import boto3

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.aws.DynamoDB.aws_dynamo_expression_builder import DynamoExpressionBuilder
from boto3.resources.model import DefinitionWithParams
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr


class DynamoDB:
    def __init__(self, table, attribute_data=None, partition_key=None, sort_key=None, projection=None, filters=None):
        self.table = table
        self.attribute_data = attribute_data
        self.partition_key = partition_key
        self.sort_key = sort_key
        self.projection = projection
        self.filters = filters
        self.dynamodb_resource = boto3.resource("dynamodb", region_name=REGION_NAME)
        self.dynamodb_table = self.dynamodb_resource.Table(self.table)
        self.builder = DynamoExpressionBuilder()

    def update(self):

        response = None
        if self.partition_key is None or self.attribute_data is None:
            return response

        expression = (
            self.builder \
                .use_key_expression(self.partition_key, self.sort_key) \
                .use_update_expression(self.attribute_data) \
                .build()
        )

        try:
            response = self.dynamodb_table.update_item(**expression)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                log_info("Item updated successfully!")
                return response

        except ClientError as error:
            error_code = error.response['Error']['Code']
            error_message = error.response['Error']['Message']
            log_error(f"Error updating item {self.attribute_data} from table {self.table}. Here's why: {error_code}: {error_message}")
            raise error
        return response

    def put(self):

        response = None
        if self.partition_key is None or self.attribute_data is None:
            return response

        expression = (
            self.builder \
                .use_condition_expression(self.partition_key) \
                .use_item(self.attribute_data) \
                .build()
        )

        try:
            response = self.dynamodb_table.put_item(**expression)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                log_info("Item added successfully!")
                return response
        except ClientError as error:
            error_code = error.response['Error']['Code']
            error_message = error.response['Error']['Message']
            log_error(f"Error adding item {self.attribute_data} to table {self.table}. Here's why: {error_code}: {error_message}")
            raise error
        return response

    def get(self):
        """
        Retrieve a single item from DynamoDB table using the provided key.
        Returns None if item not found, raises ClientError on errors.
        """
        response = None
        if self.filters is None and (self.partition_key is None or self.sort_key is None):
            return response

        expression = (
            self.builder \
                .use_key_expression(self.partition_key, self.sort_key) \
                .use_projection(self.projection) \
                .build()
        )

        try:
            response = self.dynamodb_table.get_item(**expression)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                
                if 'Item' not in response:
                    log_info(f"No item found in table {self.table} for the given key.")
                    return None
                else:
                    log_info(f"Item fetched successfully: {response}")
                    return response["Item"]

        except ClientError as error:
            error_code = error.response['Error']['Code']
            error_message = error.response['Error']['Message']
            log_error(f"Error fetching item from table {self.table}. Here's why: {error_code}: {error_message}")
            raise error
        return response

    def scan(self):

        response = None
        if self.filters is None:
            return response

        expression = (
            self.builder \
                .use_filter(self.filters) \
                .use_projection(self.projection) \
                .build()
        )

        try:
            response = self.dynamodb_table.scan(**expression)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:

                if 'Items' not in response or not response['Items']:
                    log_info(f"No records found in the table {self.table}. Table might be empty.")
                    return None
                else:
                    log_info(f"Record fetched successfully: {response}")
                    return response["Items"]

        except ClientError as error:
            error_code = error.response['Error']['Code']
            error_message = error.response['Error']['Message']
            log_error(f"Error fetching record from table {self.table}. Here's why: {error_code}: {error_message}")
            raise error
        return response

    def query(self):

        response = None
        if self.partition_key is None or self.filters is None:
            return response

        expression = (
            self.builder \
                .use_key_condition_expression(self.partition_key, self.sort_key) \
                .use_filter(self.filters) \
                .use_projection(self.projection) \
                .build()
        )

        try:
            response = self.dynamodb_table.query(**expression)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:

                if 'Items' not in response or not response['Items']:
                    log_info(f"Record not found in table {self.table}. Table might be empty.")
                    return None
                else:
                    log_info(f"Record fetched successfully: {response}")
                    return response["Items"]

        except ClientError as error:
            error_code = error.response['Error']['Code']
            error_message = error.response['Error']['Message']
            log_error(
                f"Error fetching record from table {self.table}. Here's why: {error_code}: {error_message}")
            raise error
        return response
