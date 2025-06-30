import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import VolcanicData

class MonitoringConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('monitoring', self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('monitoring', self.channel_name)
    
    async def receive(self, text_data):
        pass
    
    async def send_volcanic_data(self, event):
        await self.send(text_data=json.dumps(event['data']))
