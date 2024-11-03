# IntelliTrader\backend\models\BaseModel.py

from abc import ABC, abstractmethod
import time


class BaseModel(ABC):
    def __init__(self):
        pass
        # self.created_by = "IntelliTrader"
        # self.modified_date = time.strftime("%Y-%m-%d %H:%M:%S")

    def convert_table_rows_to_dict(self, table_configuration):
        """
        Converts the object attributes to a dictionary, including hash and sort key information.
        """
        data_dict = {}
        rows = {}
        for attr_name, attr_value in self.__dict__.items():
            if not callable(attr_value) and attr_value is not None:
                rows[attr_name] = attr_value

        data_dict["dataset_object"] = rows

        # Extract partition key information from the already created table_dataset_object
        partition_key_name = table_configuration["partition_key"]
        partition_key_value = data_dict["dataset_object"][partition_key_name]

        data_dict["partition_object"] = {
            "key_value": {
                partition_key_name: partition_key_value
            },
            "key": partition_key_name,
            "value": partition_key_value,
            "condition": {
                partition_key_name: {
                    "eq": partition_key_value
                }
            }
        }

        # Extract sort key information (if applicable)
        sort_key_name = table_configuration.get("sort_key")
        if sort_key_name:
            sort_key_value = data_dict["dataset_object"][sort_key_name]

            data_dict["sort_object"] = {
                "key_value": {
                    sort_key_name: sort_key_value
                },
                "key": sort_key_name,
                "value": sort_key_value,
                "condition": {
                    sort_key_name: {
                        "eq": sort_key_value
                    }
                }
            }
        else:
            data_dict["sort_object"] = None

        return data_dict
