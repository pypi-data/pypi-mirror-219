import json
from typing import Any, Optional

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

    def create_user(
        self,
        *,
        external_id: str,
        status: str,
        messages: Optional[str] = "0",
        emails: Optional[str] = "0"
    ) -> Any:
        data = dict(
            external_id=external_id,
            user_info=json.dumps(
                dict(
                    status=status,
                    messages=messages,
                    emails=emails
                )
            )
        )
        self.put_item(data=data)

    def update_user(
        self,
        *,
        external_id: str,
        user_info: str,
        status: str,
        messages: Optional[str] = "0",
        emails: Optional[str] = "0"
    ) -> None:
        new_user_info = json.dumps(
            dict(
                status=status,
                messages=messages,
                emails=emails
            )
        )
        self.table.update_item(
            ExpressionAttributeNames={
                '#UI': 'user_info',
            },
            ExpressionAttributeValues={
                ':user_info': {
                    'S': new_user_info,
                },
            },
            Key={
                'external_id': {
                    'S': external_id,
                }
            },
            ReturnValues='UPDATED_NEW',
            UpdateExpression='SET #UI = :user_info',
        )
