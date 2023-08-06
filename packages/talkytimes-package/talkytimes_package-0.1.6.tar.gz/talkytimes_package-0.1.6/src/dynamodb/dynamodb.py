from typing import Any

from dynamodb.base import AbstractDynamoDB


class DynamoDB(AbstractDynamoDB):
    def get_user(self, *, external_id: str) -> Any:
        data = dict(external_id=external_id)
        return self.get_item(key=data)

    def get_users(self) -> dict[str, Any]:
        response = self.table.scan()
        print(response)
        data = response.get("Items")

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data

    def create_user(self, *, external_id: str, status: str) -> Any:
        data = dict(
            external_id=external_id,
            status=status
        )
        self.put_item(data=data)

    def update_user(self, *, external_id: str, status: str) -> None:
        self.table.update_item(
            Key=dict(external_id=external_id),
            UpdateExpression="set status=:status",
            ExpressionAttributeValues={
                ':status': str(status)
            },
            ReturnValues="UPDATED_NEW"
        )

    def create_or_update(self, *, external_id: str, status: str):
        user = self.get_user(external_id=external_id)
        if user:
            self.update_user(external_id=external_id, status=status)
        else:
            self.create_user(external_id=external_id, status=status)
