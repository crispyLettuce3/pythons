
#!/usr/bin/env python
import asyncio
import websockets
from aioconsole import ainput
import json

async def hello():
    uri = "wss://hrc.osmarks.net"
    global websocket
    async with websockets.connect(uri) as websocket:
        name = input("tell me your name immediately.")
        await websocket.send(json.dumps({'type':'exist','name':name}))
#        print(f"> {name}")

        greeting = await websocket.recv()
        greeted = json.loads(greeting)
        if (greeted["type"]) == 'ok':
            print('user ' + name + ' registered successfully.')
        else:
            print(f"< {greeting}")
        global channel
        channel = input("join a channel.")
        await websocket.send(json.dumps({'type':'join_channel','channel':channel}))
#        print(f"> {channel}")

        greeting = await websocket.recv()
        greeted = json.loads(greeting)
        if (greeted["type"]) == 'channel_state':
            print('channel ' + greeted["channel"] + ' joined successfully.  \nwelcome to hrc.')
        else:
            print(f"< {greeting}")
        task1 = asyncio.create_task(
            send()
        )
        task2 = asyncio.create_task(
            receive()
        )
        await task1
        await task2
async def send():
        while True:
            message = await ainput()
            if message == '/who':
                await websocket.send(json.dumps({'type':'get_channel_state','channel':channel,'state':'users'}))
            else:
                await websocket.send(json.dumps({'type':'send_message','channel':channel,'message':message}))
            #print(f"> {message}")

           # greeting = await websocket.recv()
           # print(f"< {greeting}")

async def receive():
    while True:
        messagerec = await websocket.recv()
        messagejson = json.loads(messagerec)
        if messagejson['type'] == "message":
            print(messagejson["sender"] + '> ' + messagejson["message"])
        elif messagejson['type'] == "channel_state":
            if messagejson["state_type"] == "add":
                print('user ' + messagejson["value"] + ' has joined channel ' + channel + '.')
            elif messagejson["state_type"] == "remove":
                print('user ' + messagejson["value"] + ' has left channel ' + channel + '.')
            elif messagejson["state_type"] == "set":
                messagevalue = ' '.join(map(str, messagejson["value"]))
                print('users [' + messagevalue + '] are currently in channel ' + messagejson["channel"] + '.')
            else:
                print('unhandled state_type error:')
                print(messagerec)
                print(messagejson)
        else:
           print("unhandled type error:")
           print(messagerec)
           print(messagejson)
loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
