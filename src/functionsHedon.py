import re
from datetime import datetime

def parseReactions(text: str) -> int:
    """Parses the number of reactions from a string.

    Args:
        text (str): message.reactions

    Returns:
        int: total number of reactions
    """
    pattern = r'count=\D*(\d+)'  # Regular expression pattern to match numbers after "count=15"
    numbers = re.findall(pattern, text)
    total_sum = sum(map(int, numbers))
    return total_sum

def get_message_link(chat_id: int, message_id: int) -> str:
    """Returns the link to a message.

    Args:
        chat_id (int): chat_id
        message_id (int): message_id

    Returns:
        str: link to the message
    """
    base_url = "https://t.me/c/"
    return f"{base_url}{chat_id}/{message_id}"

def formatMessage(message: str)->list:
    """Formats the messages into a list.

    Args:
        message (str): message.text

    Returns:
        list: list of message attributes
    """
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
    list.append(message.mentioned)
    return list

def generateChannelsFile(result:telethon.tl.types.messages.DialogsSlice) -> None:
    """Generates a list of channels from the result of GetDialogsRequest.

    Args:
        result (telethon.tl.types.messages.DialogsSlice): result of GetDialogsRequest
    """
    print ("No channel list exists. Do you want to generate one? (y/n)")
    if input() == "n":
        exit()
    with open("channels.txt", "w") as f:
        for chat in result.chats:
            f.write(chat.title + "\n")
    print ("Channel list generated. Please edit channels.txt and run the script again.")
    exit()

def createListOfChannels()->list:
    """Creates a list of channels from channels.txt.

    Returns:
        list: list of channels
    """
    with open ("channels.txt", "r") as f:
        listOfChannels = f.readlines()
    listOfChannels = [x.strip() for x in listOfChannels]
    return listOfChannels

def checkChat(chat, listOfChannels:listOfChannels) -> bool:
    """Checks if the chat is a channel and if it is in the channel list.

    Args:
        chat (_type_): chat object
        listOfChannels (listOfChannels): list of channels

    Returns:
        bool: True if chat is not a channel or if it is not in the channel list
    """
    if chat.megagroup:
        print (f"{chat.title} is not a channel. Skipping...")
        return True
    elif chat.title not in listOfChannels:
        print (f"{chat.title} is not in the channel list. Skipping...")
        return True

def get_datetime_from_user(string: str) -> datetime:
    """Gets the date and time from the user.

    Args:
        string (str): Input from user

    Returns:
        datetime: datetime object
    """
    while True:
        try:
            date_string = input(string)
            datetime_obj = datetime.strptime(date_string, "%Y-%m-%d")
            if checkToday(datetime_obj):
                print ("Starting date is incorrect. Maybe date entered is in the future?")
            else:
                return datetime_obj
        except ValueError:
            print("Invalid input. Please enter the date and time in the correct format.")

def nOfDays(startDate: datetime, endDate: datetime) -> bool:
    """Checks if the number of days between the start and end date is less than or equal to 0.

    Args:
        startDate (datetime): Starting day of the period
        endDate (datetime): Ending day of the period

    Returns:
        bool: True if the number of days is less than or equal to 0
    """
    delta = endDate - startDate
    if delta.days <= 0:
        return True
    
def checkToday(date: datetime) -> bool:
    """Checks if the date is in the future.

    Args:
        date (datetime): date

    Returns:
        bool: True if the date is in the future
    """
    dayDiff = date - datetime.today()
    if dayDiff.days > 0:
        return True
    
def getDates () -> tuple:
    """Gets the start and end date from the user.

    Returns:
        tuple: start and end date
    """
    start_date = get_datetime_from_user ("Enter the starting date. The format should be YYYY-MM-DD: ")
    end_date = get_datetime_from_user ("Enter the date of the end of downloaded period. The format should be YYYY-MM-DD: ")
    return start_date, end_date
    
def printHelp():
    """Prints help information
    """
    print ("Usage: python3 hedon.py [OPTIONS]")
    print ("Options:")
    print ("  -h, --help        show this help message and exit")
    print ("  -c, --channels    generate a list of channels")
    print ("  -m, --map         generates a csv of connections")
    print ("  run without options to download messages")
    exit()
