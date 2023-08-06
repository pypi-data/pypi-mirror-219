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
        status: str,
        messages: Optional[str] = "0",
        emails: Optional[str] = "0"
    ) -> None:
        user_info = json.dumps(
            dict(
                status=status,
                messages=messages,
                emails=emails
            )
        )
        self.table.update_item(
            Key=dict(external_id=external_id),
            AttributeUpdates={
                'user_info': user_info,
            },
            ReturnValues="UPDATED_NEW"
        )

    def create_or_update(
        self,
        *,
        external_id: str,
        status: str,
        messages: Optional[str] = "0",
        emails: Optional[str] = "0"
    ):
        user = self.get_user(external_id=external_id)
        if user:
            self.update_user(
                external_id=external_id,
                status=status,
                messages=messages,
                emails=emails
            )
        else:
            self.create_user(
                external_id=external_id,
                status=status,
                messages=messages,
                emails=emails
            )
