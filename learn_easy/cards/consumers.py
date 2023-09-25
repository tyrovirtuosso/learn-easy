from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.urls import reverse

class UserNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            # Replace "@" and "." in the email with "_" as "@" symbol as it is not a valid character for a group name in Django Channels
            email = self.user.email.replace("@", "_").replace(".", "_")
            await self.channel_layer.group_add(
                f"user_{email}",  # Unique group for this user
                self.channel_name)
            await self.accept()
        else:
            await self.close()
            
    async def disconnect(self, close_code):
        self.user = self.scope["user"]
        email = self.user.email.replace("@", "_").replace(".", "_")
        await self.channel_layer.group_discard(f"user_{email}", self.channel_name)
    
    async def item_update(self, event):
        card = event["card"]
        await self.send(text_data=json.dumps({
            "type": str(event["type"]),
            "pk": card.pk,
            "word": card.word,
            "category": card.category,
            "meaning": "" if card.meaning.lower() == "not specified" else card.meaning,
            "detail_url": reverse('items:item_detail', args=[card.pk]),
            "delete_url": reverse('items:delete_item', args=[card.pk]),
        }))

                
            
        

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("notifications", self.channel_name)
    
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("notifications", self.channel_name)
    
#     #This method is called when a message is sent to the "notifications" group.
#     async def send_notification(self, event):
#         message = event["message"]

#         template = Template('<div class="notification"><p>{{message}}</p></div>')
#         context = Context({"message":message})
#         rendered_notification = template.render(context)

#         # This line is sending a message over the WebSocket.
#         await self.send(
#             text_data=json.dumps(
#             {
#                 "type": "notification",
#                 "message": rendered_notification,
#                 "item_id": event.get("item_id"),
#                 "category": event.get("category"),
#                 "word": event.get("word")
#             }
#             )
#         )
        