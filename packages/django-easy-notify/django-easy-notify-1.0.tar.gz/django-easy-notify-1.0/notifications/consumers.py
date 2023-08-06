import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from notifications.models import Notification


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    # Function to connect to the websocket
    async def connect(self):
        # Checking if the User is logged in
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        if not self.user_id:
            # Reject the connection
            await self.close()
        else:
            self.room_group_name = f"notifications_{self.user_id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    # Function to disconnet the Socket
    async def disconnect(self, close_code):
        await self.close()

    def get_async_notifications(self):
        self.notifications = list(
            Notification.objects.prefetch_related("receivers")
            .filter(
                receivers__id__in=[int(self.user_id)],
                state=Notification.NotificationState.unread,
            )
            .values("title", "message", "notification_type")
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json["command"]
        # Send message to room group
        if command == "new_notification":
            content = text_data_json["content"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "notify", "content": [content], "command": command},
            )
        elif command == "fetch_all_notifications":
            await database_sync_to_async(self.get_async_notifications)()
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "notify", "content": self.notifications, "command": command},
            )

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    async def notify(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "content": event["content"],
                }
            )
        )
