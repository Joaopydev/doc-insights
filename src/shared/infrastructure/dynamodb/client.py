import boto3

from src.shared.application.ports.db_client import DBClient


class DynamoDBClient(DBClient):

    def __init__(self):
        self.__dynamodb_resource = boto3.resource("dynamodb")

    def save(self, table_name: str, item: dict):
        table = self.__get_table(table_name)
        table.put_item(Item=item)

    def __get_table(self, table_name: str):
        return self.__dynamodb_resource.Table(table_name)
