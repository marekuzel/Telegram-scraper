import configparser
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest

from messageFormater import formatMessage
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
        limit=100,
        hash=0,
    ))

with TelegramClient(username, api_id, api_hash) as client:
    for chat in result.chats:
        max_messages = 100
        d = {}
        print (f"{chat.title} in progress...")
        for message in client.iter_messages(chat.id): 
            if len(message.text) < 5:
                continue
            d["message{0}".format(message.id)] = formatMessage(message)
            max_messages -= 1
            if max_messages == 0:
                break

with open('data.csv', 'w') as f:
    f.write("Author, Title, Interactions, Views, Date, Message body\n")
    for line in d:
        for data in d[line]:
            f.write(f'"{data}",')
        f.write("\n")