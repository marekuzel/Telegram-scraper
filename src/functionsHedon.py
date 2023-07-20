import re
from datetime import datetime
def parseReactions(text):
    pattern = r'count=\D*(\d+)'  # Regular expression pattern to match numbers after "count=15"
    numbers = re.findall(pattern, text)
    total_sum = sum(map(int, numbers))
    return total_sum

def get_message_link(chat_id, message_id):
    base_url = "https://t.me/c/"
    return f"{base_url}{chat_id}/{message_id}"

def formatMessage(message):
    list = []
    title = str(message.text).split(" ")
    msg_title = " ".join(title[:4])
    list.append(message.sender.username) 
    list.append(msg_title)
    list.append(parseReactions(str(message.reactions)))
    list.append(message.views)
    list.append(str(message.date.replace(tzinfo=None)))
    list.append(message.text)
    list.append(get_message_link(message.chat.id, message.id))
    return list

def generateChannelsFile(result):
    print ("No channel list exists. Do you want to generate one? (y/n)")
    if input() == "n":
        exit()
    with open("channels.txt", "w") as f:
        for chat in result.chats:
            f.write(chat.title + "\n")
    print ("Channel list generated. Please edit channels.txt and run the script again.")
    exit()

def createListOfChannels():
    with open ("channels.txt", "r") as f:
        listOfChannels = f.readlines()
    listOfChannels = [x.strip() for x in listOfChannels]
    return listOfChannels

def checkChat(chat, listOfChannels):
    if chat.megagroup:
        print (f"{chat.title} is not a channel. Skipping...")
        return True
    elif chat.title not in listOfChannels:
        print (f"{chat.title} is not in the channel list. Skipping...")
        return True

def get_datetime_from_user(string):
    while True:
        try:
            date_string = input(string)
            datetime_obj = datetime.strptime(date_string, "%Y-%m-%d")
            return datetime_obj
        except ValueError:
            print("Invalid input. Please enter the date and time in the correct format.")

def nOfDays(startDate, endDate):
    delta = endDate - startDate
    if delta.days >= 0:
        return True
def checkToday(date):
    dayDiff = date - datetime.today()
    if dayDiff.days > 0:
        return True