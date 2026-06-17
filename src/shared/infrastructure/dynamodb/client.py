import boto3
from boto3.dynamodb.conditions import Key

from src.shared.application.ports.db_client import DBClient


class DynamoDBClient(DBClient):

    def __init__(self):
        self.__dynamodb_resource = boto3.resource("dynamodb")

    def save(self, table_name: str, item: dict):
        table = self._get_table(table_name)
        table.put_item(Item=item)

    def get_item(self, table_name, key):
        table = self._get_table(table_name)
        response = table.get_item(Key=key)
        return response.get("Item")

    def query(self, table_name: str, index_name: str, key_name: str, key_value: str):
        table = self._get_table(table_name)
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=Key(key_name).eq(key_value)
        )
        items = response.get("Items", [])

        return items[0] if items else None


    def _get_table(self, table_name: str):
        return self.__dynamodb_resource.Table(table_name)
