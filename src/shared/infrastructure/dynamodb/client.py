import boto3


class DynamoDBClient:
    def __init__(self):
        self.dynamodb_resource = boto3.resource("dynamodb")

    def get_table(self, table_name: str):
        return self.dynamodb_resource.Table(table_name)

    def put_item(self, table_name: str, item: dict):
        table = self.get_table(table_name)
        table.put_item(Item=item)
