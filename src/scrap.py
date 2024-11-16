#!/usr/bin/python3

import os
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from datetime import datetime
import argparse

from scraper_lib import *


def main():
    d = {} #dictionary to store messages

    api_id, api_hash, username = getConfig()

    #gets the api_id and api_hash
    with TelegramClient(username, api_id, api_hash) as client:
        result = client(GetDialogsRequest(
            offset_date=0,
            offset_id=0,
            offset_peer="username",
            limit=100,
            hash=0,
        ))

    parser = argparse.ArgumentParser(description="Downloads messages from telegram chats and saves them to a csv file")
    parser.add_argument("-c", "--channels", help="Creates a file with the list of channels", action="store_true")
    parser.add_argument("-s", "--simpleData", help="Generates less extensive table. Contains only essential information.")
    args = parser.parse_args()
    if args.channels:
        generateChannelsFile(result)
        exit()

    #checks if the channels file exists and create list of channels
    listOfChannels = tryListOfChannels(result)

    #check if the channels selected should be downloaded
    if channelVerif(result, listOfChannels):
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
            dt = collectData(chat.id, client, start_date, end_date)
    #writing to csv file
    #simpleCsvWriter(d)
    pd.DataFrame.to_csv(dt)
if __name__ == "__main__":
    main()