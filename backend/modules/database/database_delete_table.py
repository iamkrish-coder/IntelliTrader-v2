# database_delete_table.py

from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from backend.utils.caching_utils import *
from boto3.exceptions import botocore
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

import boto3
import json


class DatabaseDeleteTable:
    def __init__(self, table_configuration):
        self.dynamodb_resource = boto3.resource('dynamodb', region_name=REGION_NAME)
        self.table_configuration = table_configuration
        self.table_name = None

    def initialize(self, table_names):
        for self.table_name in table_names:
            if not self.delete_tables():
                return False

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

    def delete_tables(self):
        if self.table_name is not None:
            """ Check If Table Exists """
            table_exists = self.check_table_exists()
            if table_exists:
                try:
                    response = self.dynamodb_resource.Table(self.table_name).delete()
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        try:
                            self.dynamodb_resource.Table(self.table_name).wait_until_not_exists(WaiterConfig={'Delay': 2})
                            log_info(f"Delete '{self.table_name}' table ...COMPLETE!")
                        except ClientError as error:
                            if error.response['Error']['Code'] != 'ResourceNotFoundException':
                                return False
                        self.delete_table_cache()
                        self.delete_table_configuration()
                        return True
                except ClientError as error:
                    log_error(f"Error deleting table {self.table_name}. Here's why: {error.response["Error"]["Code"]}: {error.response["Error"]["Message"]}")
                    return False

    def delete_table_cache(self):
        deleted_table_name = cache_directory = self.table_name
        cache_directory = self.table_name
        remove_cache(Cache_Type.DISK.value, cache_directory)
        log_info(f"Delete '{deleted_table_name}' cache ...COMPLETE!")

    def delete_table_configuration(self):
        deleted_table_name = self.table_name

        # Read the config file
        with open(CONFIGURATION_PATH + '/' + TABLE_CONFIGURATION_FILE, 'r') as file:
            config_data = json.load(file)

        # Check if the deleted table name exists in the config
        if deleted_table_name in config_data:
            # Remove the entry associated with the deleted table name
            # del config_data[deleted_table_name] # Commented out for now
            log_info(f"Delete '{deleted_table_name}' configuration ...COMPLETE!")
        else:
            log_info(f"Table '{deleted_table_name}' not found in the configuration.")

        # Write the updated config back to the file
        with open(CONFIGURATION_PATH + '/' + TABLE_CONFIGURATION_FILE, 'w') as file:
            json.dump(config_data, file, indent=4)
