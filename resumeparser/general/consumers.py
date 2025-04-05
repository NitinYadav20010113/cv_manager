import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from . tblmodels import process_information


class FileProgressConsumer(WebsocketConsumer):
    def connect(self):
        print('connected')
        self.group_name = 'file_progress'
        
        # Join the group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()
    
    def disconnect(self, close_code):
        # Leave the group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
    
    def progress_update(self, event):
        
        user = event['user']
        prog=event['prog']
        disable=event['disable']
        
        data=process_information.objects.get(user=user)
        completed=data.file_completed
        total=data.total_files
        print(' UPDATE PROGRESS :The completed files are',completed,'The total files are',total)
        # Send progress update to WebSocket
        self.send(text_data=json.dumps({
            'completed': completed,
            'total': total,
            'prog':prog,
            'disable':disable
        }))
