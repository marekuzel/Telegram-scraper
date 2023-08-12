import os
import configparser
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from functionsHedon import *
import csv
from datetime import datetime
import sys
#checks for arguments
if len(sys.argv) == 2:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        printHelp()
    elif sys.argv[1] == "-c" or sys.argv[1] == "--channels":
        #TODO: generateChannelsFile()
        print ("developer was lazy and this feature is to be impemented in the future....")
        exit()

#checks for config file
if not os.path.isfile("config.ini"):
    print("Error: config.ini file not found. config.ini file must be in the same directory as hedon.py, and must contain API id and API hash")
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

#gets the api_id and api_hash
with TelegramClient(username, api_id, api_hash) as client:
    result = client(GetDialogsRequest(
        offset_date=0,
        offset_id=0,
        offset_peer="username",
        limit=100,
        hash=0,
    ))

#checks if the channels file exists, if not, generates it
try:
    listOfChannels = createListOfChannels()
except FileNotFoundError:
    generateChannelsFile(result)
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

# gets the start and end dates from the user
start_date, end_date = getDates()
if nOfDays(start_date, end_date):
    print ("The start date should be before the end date")
    exit()

#goes through the chats and messages and adds them to a dictionary
with TelegramClient(username, api_id, api_hash) as client:
    for chat in result.chats:
        if checkChat(chat, listOfChannels):
            continue
        print (f"{chat.title} in progress...")
        for message in client.iter_messages(chat.id):
            if message.date.replace(tzinfo=None) > end_date:
                print (message)
                continue
            elif message.date.replace(tzinfo=None) < start_date:
                break
            if len(str(message.text)) < 5:
                continue
            d["message{0}".format(message.id)] = formatMessage(message)
            
#writing to csv file
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Author", "Title", "Interactions", "Views", "Date", "Message body", "Link"])
    for line in d.values():
        writer.writerow(line)