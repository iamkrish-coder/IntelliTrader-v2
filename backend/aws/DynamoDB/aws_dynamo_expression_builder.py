from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *
from boto3.dynamodb.conditions import Key, Attr


class DynamoExpressionBuilder:
    def __init__(self):
        self.item = None
        self.key = None
        self.condition_expression = None
        self.key_condition_expression = None
        self.update_expression = None
        self.filter_expression = None
        self.projection_expression = None
        self.expression_attribute_names = {}
        self.expression_attribute_values = {}
        self.comparison_operators = {
            "eq": "=",
            "gt": ">",
            "lt": "<",
            "gte": ">=",
            "lte": "<=",
            "le": "<=",
            "ge": ">=",
            "begins_with": "BEGINS_WITH",
            "between": "BETWEEN",
            "contains": "CONTAINS",
            "exists": "EXISTS",
            "in": "IN",
        }

    def use_key_expression(self, partition_key, sort_key):
        key = {}
        if partition_key:
            key[partition_key['key']] = partition_key['value']

        if sort_key:
            key[sort_key['key']] = sort_key['value']

        self.key = key
        return self

    def use_update_expression(self, attribute_data):
        update_expression = "SET "
        expression_attribute_values = {}
        counter = 0

        for attribute_path, new_value in attribute_data.items():
            counter += 1
            placeholder = f":v{counter}"
            update_expression += f"{attribute_path}={placeholder}, "
            expression_attribute_values[placeholder] = new_value

        if counter > 0:
            update_expression = update_expression.rstrip(", ")

        self.update_expression = update_expression
        self.expression_attribute_values.update(expression_attribute_values)
        return self

    def use_item(self, item):
        self.item = item
        return self

    def use_condition_expression(self, partition_key):
        self.condition_expression = Attr(partition_key['key']).not_exists()
        return self

    def use_key_condition_expression(self, partition_key, sort_key):

        partition_key_name = partition_key['key']
        partition_key_value = partition_key['value']

        # Build the KeyConditionExpression dynamically
        key_condition_expression = Key(partition_key_name).eq(partition_key_value)

        if sort_key and sort_key is not None:
            for key, value in sort_key["condition"].items():
                if isinstance(value, dict) and "between" in value:
                    operator, min_val, max_val = "between", value["between"]["min"], value["between"]["max"]
                    condition = Key(key).between(min_val, max_val)
                elif isinstance(value, dict):
                    operator, val = list(value.items())[0]
                    condition = getattr(Key(key), operator)(val)
                else:
                    condition = Key(key).eq(value)

                key_condition_expression &= condition

        self.key_condition_expression = key_condition_expression
        return self

    def use_projection(self, fields=None):
        if fields is not None:
            projection_fields = ", ".join(fields)
            self.projection_expression = projection_fields
        return self

    def use_filter(self, filters):
        filter_expression = ""
        expression_attribute_names = {}
        expression_attribute_values = {}

        is_first_condition = True
        for key, value in filters.items():

            if isinstance(value, dict) and "between" in value:
                operator, min_val, max_val = "between", value["between"]["min"], value["between"]["max"]
                cond = f"{key} {self.comparison_operators[operator]} :min_{key} AND :max_{key}"
                expression_attribute_values[f":min_{key}"] = min_val
                expression_attribute_values[f":max_{key}"] = max_val
            elif isinstance(value, dict):
                operator, val = list(value.items())[0]
                cond = f"{key} {self.comparison_operators[operator]} :{key}"
                expression_attribute_values[f":{key}"] = val
            else:
                cond = f"{key} = :{key}"
                expression_attribute_values[f":{key}"] = value

            if not is_first_condition:
                filter_expression += " AND "

            filter_expression += cond
            is_first_condition = False

        if filter_expression != "":
            self.filter_expression = filter_expression
            self.expression_attribute_names.update(expression_attribute_names)
            self.expression_attribute_values.update(expression_attribute_values)

        return self

    def build(self):
        return {
            key: value for key, value in {
                "Key": self.key,
                "Item": self.item,
                "ConditionExpression": self.condition_expression,
                "KeyConditionExpression": self.key_condition_expression,
                "UpdateExpression": self.update_expression,
                "FilterExpression": self.filter_expression,
                "ProjectionExpression": self.projection_expression,
                "ExpressionAttributeNames": self.expression_attribute_names if self.expression_attribute_names else None,
                "ExpressionAttributeValues": self.expression_attribute_values if self.expression_attribute_values else None,
            }.items() if value is not None
        }
