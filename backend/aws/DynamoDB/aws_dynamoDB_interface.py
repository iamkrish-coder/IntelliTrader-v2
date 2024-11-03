# backend/aws/DynamoDB/aws_dynamoDBInterface.py

class DynamoDBInterface:
    def check_table_exists(self):
        raise NotImplementedError("Method not implemented")

    def create_table(self, table_properties):
        raise NotImplementedError("Method not implemented")

    def delete_table(self):
        raise NotImplementedError("Method not implemented")

    def put_item(self, item):
        raise NotImplementedError("Method not implemented")

    def query_items(self, **arguments):
        raise NotImplementedError("Method not implemented")

    def get_item(self, key_expression):
        raise NotImplementedError("Method not implemented")

    def scan_items(self, **kwargs):
        raise NotImplementedError("Method not implemented")

    def update_item(self, key, update_expression, **kwargs):
        raise NotImplementedError("Method not implemented")

    def delete_item(self, key):
        raise NotImplementedError("Method not implemented")
