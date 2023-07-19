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
    
try:
    with open ("channels.txt", "r") as f:
        listOfChannels = f.readlines()
        listOfChannels = [x.strip() for x in listOfChannels]
except FileNotFoundError:
    print ("No channel list exists. Do you want to generate one? (y/n)")
    if input() == "n":
        exit()
    with open("channels.txt", "w") as f:
        for chat in result.chats:
            f.write(chat.title + "\n")
except IOError as e:
    print(f"An error occurred: {str(e)}")

d = {}

for chat in result.chats:
    if str(chat.title) in listOfChannels:
        print (chat.title)
    else:
        print (f"{chat.title} not selected")
print ("-------------------------------------------------------------------------------")
print ("These are the channels picked up by the script. Do you want to continue? (y/n)")
if input() == "n":
    exit()
    
with TelegramClient(username, api_id, api_hash) as client:
    for chat in result.chats:
        if chat.megagroup:
            print (f"{chat.title} is not a channel. Skipping...")
            continue
        elif chat.title not in listOfChannels:
            print (f"{chat.title} is not in the list of channels. Skipping...")
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