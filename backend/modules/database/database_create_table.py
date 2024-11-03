# database_create_table.py

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from boto3.exceptions import botocore
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

import boto3


class DatabaseCreateTable:
    def __init__(self, table_configuration):
        self.dynamodb_resource = boto3.resource('dynamodb', region_name=REGION_NAME)
        self.table_configuration = table_configuration
        self.table_name = None

    def initialize(self, table_names):
        for self.table_name in table_names:
            self.create_tables()

    def check_table_exists(self):
        try:
            self.dynamodb_resource.Table(self.table_name).load()
            exists = True
        except ClientError as error:
            if error.response['Error']['Code'] == 'ResourceNotFoundException':
                exists = False
            else:
                log_error("Couldn't check for existence of %s. Here's why: %s: %s", self.table_name, error.response["Error"]["Code"], error.response["Error"]["Message"])
                raise error
        return exists

    def create_tables(self):
        """ Check If Table Exists """
        table_exists = self.check_table_exists()
        if not table_exists:
            table_properties = {}
            table_properties = self.build_table_definition()
            try:
                response = self.dynamodb_resource.create_table(
                    TableName=self.table_name,
                    KeySchema=table_properties['table_schema'],
                    AttributeDefinitions=table_properties['attribute_definitions'],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
                response.wait_until_exists()
                log_info(f"Create '{self.table_name}' table ...COMPLETE!")

            except ClientError as error:
                log_error(
                    f"Error creating table {self.table_name}. Here's why: {error.response["Error"]["Code"]}: {error.response["Error"]["Message"]}")
                raise error
        else:
            log_info(f"Table '{self.table_name}' already exists.")

    def build_table_definition(self):

        table_config = self.table_configuration[self.table_name]
        table_key_name = table_config['table_key']
        partition_key_name = table_config['partition_key']
        sort_key_name = table_config['sort_key']

        table_definition = {
            'table_name': table_key_name,
            'table_schema': [
                {
                    'AttributeName': partition_key_name,
                    'KeyType': 'HASH'
                },
                # Only include sort key definition if sort_key_name is not empty
                *([
                      {
                          'AttributeName': sort_key_name,
                          'KeyType': 'RANGE'
                      }
                  ] if sort_key_name else [])
            ],
            'attribute_definitions': [
                {
                    'AttributeName': partition_key_name,
                    'AttributeType': 'S'
                },
                # Only include sort key attribute definition if sort_key_name is not empty
                *([
                      {
                          'AttributeName': sort_key_name,
                          'AttributeType': 'S'
                      }
                  ] if sort_key_name else [])
            ]
        }

        return table_definition