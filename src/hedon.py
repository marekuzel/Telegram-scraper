import os
import configparser
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from functionsHedon import *
import csv
from datetime import datetime
import sys

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
names = False
#checks for arguments
if len(sys.argv) == 2:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        printHelp()
    elif sys.argv[1] == "-c" or sys.argv[1] == "--channels":
        generateChannelsFile(result)
        exit()
    elif sys.argv[1] == "-m" or sys.argv[1] == "--map":
        runMap(result.chats, TelegramClient(username, api_id, api_hash))
    elif sys.argv[1] == "-n" or sys.argv[1] == "--names":
        names = True
        
#checks if the channels file exists and create list of channels
listOfChannels = tryListOfChannels(result)

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
subjects = {}
#goes through the chats and messages and adds them to a dictionary
with TelegramClient(username, api_id, api_hash) as client:
    for chat in result.chats:
        if checkChat(chat, listOfChannels):
            continue
        print (f"{chat.title} in progress...")
        for message in client.iter_messages(chat.id):
            if message.date.replace(tzinfo=None) > end_date:
                continue
            elif message.date.replace(tzinfo=None) < start_date:
                break
            if len(str(message.text)) < 5:
                continue
            if names:
                subjectsPerMessage = countSubjects(message.text)
                for name in subjectsPerMessage:
                    if name not in subjects:
                        subjects[name] = subjectsPerMessage[name]
                    else:
                        subjects[name] += subjectsPerMessage[name]
            else:
                subjectsPerMessage ={}
            d["message{0}".format(message.id)] = formatMessage(message, names, subjectsPerMessage, client)
            subjectsPerMessage = {key: 0 for key in subjectsPerMessage}
#writing to csv file
if names:
    print (subjects)
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    listOfHeadings = ["Author", "Title", "Interactions", "Views", "Date", "Message body", "Link", "Forward from"]
    for subject in subjects:
        listOfHeadings.append(subject)
    writer.writerow(listOfHeadings)
    for line in d.values():
        writer.writerow(line)