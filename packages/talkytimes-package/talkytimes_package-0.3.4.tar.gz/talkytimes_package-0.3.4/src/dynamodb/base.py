import abc
from typing import Any, Optional

import boto3


class AbstractDynamoDB(abc.ABC):
    def __init__(self, table: str):
        db = boto3.resource("dynamodb")
        self.table = db.Table(table)

    def put_item(self, *, data: dict[str, Any]) -> None:
        self.table.put_item(Item=data)

    def get_item(self, *, key: dict[str, Any]) -> Optional[Any]:
        try:
            return self.table.get_item(Key=key)
        except:
            pass
        return None
