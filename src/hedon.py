import configparser
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest

from messageFormater import parseReactions
config = configparser.ConfigParser()
config.read("config.ini")
api_id: str = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

with TelegramClient(username, api_id, api_hash) as client:
    result = client(GetDialogsRequest(
        offset_date=0,
        offset_id=0,
        offset_peer="username",
        limit=5,
        hash=0,
    ))


with TelegramClient(username, api_id, api_hash) as client:
    for chat in result.chats:
        print(chat.title)
        max_messages = 100
        d = {}
        for message in client.iter_messages(chat.id):
            d["message{0}".format(message.id)] = []
            d["message{0}".format(message.id)].append(message.text)
            d["message{0}".format(message.id)].append(parseReactions(str(message.reactions)))
            d["message{0}".format(message.id)].append(message.date)
            d["message{0}".format(message.id)].append(message.views)
            max_messages -= 1
            if max_messages == 0:
                print (d)
                break
        