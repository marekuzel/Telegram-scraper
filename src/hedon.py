import os
import configparser
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from messageFormater import formatMessage
import csv

if not os.path.isfile("config.ini"):
    print("Error: config.ini file not found.")
    exit()


config = configparser.ConfigParser()
try:
    config.read("config.ini")
    api_id: str = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']
except configparser.Error as e:
    print(f"Error reading configuration: {str(e)}")
    exit()

with TelegramClient(username, api_id, api_hash) as client:
    result = client(GetDialogsRequest(
        offset_date=0,
        offset_id=0,
        offset_peer="username",
        limit=100,
        hash=0,
    ))
d = {}
with TelegramClient(username, api_id, api_hash) as client:
    for chat in result.chats:
        if chat.megagroup:
            print (f"{chat.title} is not a channel. Skipping...")
            continue
        max_messages = 100
        print (f"{chat.title} in progress...")
        for message in client.iter_messages(chat.id): 
            if len(message.text) < 5:
                continue
            d["message{0}".format(message.id)] = formatMessage(message)
            max_messages -= 1
            if max_messages == 0:
                break

with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Author", "Title", "Interactions", "Views", "Date", "Message body"])
    for line in d.values():
        writer.writerow(line)