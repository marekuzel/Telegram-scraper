#!/usr/bin/python3

import os
import asyncio
from telethon import TelegramClient 
from telethon.tl.functions.messages import GetDialogsRequest
from datetime import datetime
import argparse

from scraper_lib import *


async def main():
    d = {} 
    api_id, api_hash, username = getConfig()

    client = TelegramClient(username, api_id, api_hash)
    
    async with client:

        result = await client(GetDialogsRequest(
            offset_date=0,
            offset_id=0,
            offset_peer="username",
            limit=100,
            hash=0,
        ))

        parser = argparse.ArgumentParser(description="Downloads messages...")
        parser.add_argument("-c", "--channels", help="Creates a file...", action="store_true")
        parser.add_argument("-s", "--simpleData", help="Generates less extensive table...")
        args = parser.parse_args()

        if args.channels:
            generateChannelsFile(result)
            return

        listOfChannels = tryListOfChannels(result)

        if channelVerif(result, listOfChannels):
            return

        start_date, end_date = getDates()
        if nOfDays(start_date, end_date):
            print("The start date should be before the end date")
            return

        for chat in result.chats:
            if checkChat(chat, listOfChannels):
                continue
            print(f"{chat.title} in progress...")
            try:
                async for message in client.iter_messages(chat.id):
                    if message.date.replace(tzinfo=None) > end_date:
                        continue
                    elif message.date.replace(tzinfo=None) < start_date:
                        break

                    d["message{0}".format(message.id)] = await formatMessage(message, client)

            except Exception as e:
                print(f"Error in {chat.title}: {e}")
        
        simpleCsvWriter(d)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass