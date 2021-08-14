from discord_webhook import DiscordWebhook
from urllib.request import urlopen
import json
import time

url1 = "http://192.168.1.172:7590/radio/getpic"
url2 = "http://192.168.1.172:7590/radio/update_radio"  
webhookurl = "https://discord.com/api/webhooks/875922156985405521/YLAxAeWn2l1J_AzAamhEKWZIgys7Ydh_iQyTSNPA8DbrS29PesPFbpNGZ5hi94LwWfBN"  

while True:
    page1 = urlopen(url1)
    page2 = urlopen(url2)

    html_bytes1 = page1.read() 
    html1 = html_bytes1.decode("utf-8")
    jsonthe1 = json.loads(html1)

    html_bytes2 = page2.read()
    html2 = html_bytes2.decode("utf-8")
    jsonthe2 = json.loads(html2)
    
    #print('the')
    #print(str(jsonthe2['index']))

    with open('./info.txt', "r") as info:
        data = info.read()

    if data != str(jsonthe2['index']):
        with open('./info.txt', "w") as info:
            info.write(str(jsonthe2['index']))
        #print(jsonthe2)
        album = str(jsonthe1['album'])
        title = str(jsonthe1['title'])
        print(album)
        print(title)
        webhook = DiscordWebhook(url=webhookurl, content="[song change!](https://waso.69.mu/radio) \n" + "title: " + title + "\n" + "album: " + album)
        webhook.execute()
        #print("update!" + data)
    time.sleep(5)
