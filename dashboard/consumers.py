import json
import threading
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import DeviceInfo


class DisplayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'display_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print ("receive")
        print (self.room_group_name, text_data)
        type_name = ''
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message['message'] == "Search Device":
            type_name = 'search_device'
        elif message['message'] == "Stop Search Device":
            self.start_search = False
        elif message['message'] == "Delete Device":
            type_name = 'delete_device'
        elif message['message'] == "Add Device":
            type_name = 'add_device'
        elif message['message'] == "Allow Device":
            type_name = 'allow_device'

        if type_name:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': type_name,
                    'message': message
                }
            )

    async def display_data(self, event):
        print ('display info!')
        msg_json = event['message']
        if isinstance(msg_json, str):
            msg_json = json.loads(msg_json)
        # msg_json = json.dumps(msg_json)
        await self.send(text_data=json.dumps({
            'message': msg_json
        }))

    async def search_device(self, event):
        msg_json = event['message']
        # if isinstance(msg_json, str):
        #     msg_json = json.loads(msg_json)
        # print ("search", msg_json)
        # info = msg_json['message']
        from .mqtt import pub_client
        pub_client.publish ("server/search/info", payload=json.dumps(msg_json), qos=0)

    async def find_device(self, event):
        print ("Find Device!!!")
        msg_json = event['message']
        if isinstance(msg_json, str):
            msg_json = json.loads(msg_json)
        await self.send(text_data=json.dumps({
            'message': msg_json
        }))

    async def delete_device(self, event):
        msg_json = event['message']
        if isinstance(msg_json, str):
            msg_json = json.loads(msg_json)
        uuid = msg_json['uuid']
        device_exist = DeviceInfo.objects.filter(uuid=uuid)

        if device_exist and device_exist[0].online:
            # info = "Delete Device " + msg_json['uuid']
            from .mqtt import pub_client
            pub_client.publish("server/delete/info", payload=json.dumps(msg_json), qos=0)

    async def add_device(self, event):
        msg_json = event['message']
        if isinstance(msg_json, str):
            msg_json = json.loads(msg_json)
        uuid = msg_json['uuid']
        device_exist = DeviceInfo.objects.filter(uuid=uuid)

        if device_exist and device_exist[0].online:
            # info = "Add Device " + msg_json['uuid']
            from .mqtt import pub_client
            pub_client.publish("server/add/info", payload=json.dumps(msg_json), qos=0)

    async def allow_device(self, event):
        msg_json = event['message']
        if isinstance(msg_json, str):
            msg_json = json.loads(msg_json)
        uuid = msg_json['uuid']
        device_exist = DeviceInfo.objects.filter(uuid=uuid)

        if not device_exist:
            # info = "Allow Device " + msg_json['uuid']
            from .mqtt import pub_client
            pub_client.publish("server/allow/info", payload=json.dumps(msg_json), qos=0)


class SearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'search_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print ("receive", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'search_device',
                'message': message
            }
        )

    async def search_device(self, event):
        msg_json = event['message']
        if isinstance(msg_json, str):
            msg_json = json.loads(msg_json)
        print ("search", msg_json)
        if msg_json['message'] == "Search Device":
            info = msg_json['message']
            self.start_search = True
            self.search_t = threading.Thread(target=self.searchDevice_thread, args=(info,), kwargs={})
            self.search_t.setDaemon(True)
            self.search_t.start()
        elif msg_json['message'] == "Stop Search Device":
            self.start_search = False
        elif msg_json['message'] == "Find Device":
            print ("Find Device!!!")
            # if not hasattr(self, 'temp_device'):
            #     self.temp_device = dict()
            # self.temp_device[msg_json['uuid']] = dict()
            # self.temp_device[msg_json['uuid']]['host'] = msg_json['host']
            # self.temp_device[msg_json['uuid']]['os_name'] = msg_json['os_name']
            await self.send(text_data=json.dumps({
                'message': msg_json
            }))
        elif msg_json['message'] == "Allow Device":
            info = "Allow Device " + msg_json['uuid']
            from .mqtt import pub_client
            pub_client.publish("server/search/info", payload=info, qos=0)

        # await self.send(text_data=json.dumps({
        #     'message': info
        # }))
