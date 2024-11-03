import pandas as pd
import os
import json
import datetime
import time
from backend.constants.const import *
from backend.utils.logging_utils import *


class Helper:
    def __init__(self, params=None):
        self.prop = params
        self.create_output_directory()

    def create_output_directory(self):
        if not os.path.exists(OUTPUT_PATH):
            os.mkdir(OUTPUT_PATH)

    def write_text_output(self, filename, data):
        with open(os.path.join(OUTPUT_PATH, filename), 'w') as file:
            if isinstance(data, dict) or isinstance(data, list):
                json.dump(data, file, indent=4)
            else:
                file.write(str(data))

    def write_token_output(self, filename, data):
        now = datetime.datetime.now()
        CURRENT_DATE = now.strftime("%Y-%m-%d")
        connection_cache_path = os.path.join(CACHE_PATH, CURRENT_DATE, CACHE_CONNECTION_DIR)
        try:
            os.makedirs(connection_cache_path, exist_ok=True)
        except OSError as error:
            print(f"Error creating directory: {error}")

        with open(os.path.join(connection_cache_path, filename), 'w') as file:
            if isinstance(data, dict):
                json.dump(data, file, indent=4)
            else:
                file.write(str(data))

    def write_csv_output(self, filename, data):
        csv_data = pd.DataFrame(data)
        if filename.endswith('.csv'):
            csv_data.to_csv(os.path.join(OUTPUT_PATH, filename), index=False)
        else:
            symbol = filename.split("_")[1]
            os.makedirs(symbol, exist_ok=True)
            full_path = os.path.join(OUTPUT_PATH, filename)
            csv_data.to_csv(full_path, index=False)

    def convert_enum_to_class_name(self, enum_name):
        words = str(enum_name).split('_')
        converted = ''.join(word.capitalize() for word in words)
        return converted

    def get_execution_time(self, start_time, end_time):
        return end_time - start_time
        # start_time = time.time()                 
        # end_time = time.time()
        # execution_time = end_time - start_time
        # log_info(f"Execution time: {execution_time} seconds")

    def format_json_output_print(self, dictionary_data, label, prettier=False, indent=4):
        """
        Formats JSON data into a human-readable string.

        Parameters:
        - dictionary_data (str): JSON data as a string.
        - indent (int): Number of spaces to use for indentation (default is 4).

        Returns:
        - str: Formatted JSON string.
        """

        try:
            # Convert the dictionary back to a formatted JSON string
            if prettier:
                formatted_json = json.dumps(dictionary_data, indent=indent)
            else:
                formatted_json = dictionary_data

            print(f"\n ******** {label} ********\n")
            print(formatted_json)

        except Exception as error:
            log_error(f"Error occurred while formatting data: {str(error)}")