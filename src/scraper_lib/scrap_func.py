
from datetime import datetime
import configparser
import os



def generateChannelsFile(result) -> None:
    """Generates a list of channels from the result of GetDialogsRequest.

    Args:
        result (): result of GetDialogsRequest
    """
    print ("Do you want to generate channel.txt? (y/n)")
    if input() == "n":
        exit()
    with open("channels.txt", "w", encoding="utf8") as f:
        for chat in result.chats:
            try:
                f.write(chat.title + "\n")
            except:
                continue
    print ("Channel list generated. Please edit channels.txt and run the script again.")
    exit()


def createListOfChannels()->list:
    """Creates a list of channels from channels.txt.

    Returns:
        list: list of channels
    """
    with open ("channels.txt", "r",encoding="utf8") as f:
        listOfChannels = f.readlines()
    listOfChannels = [x.strip() for x in listOfChannels]
    return listOfChannels


def checkChat(chat, listOfChannels:list) -> bool:
    """Checks if the chat is a channel and if it is in the channel list.

    Args:
        chat (_type_): chat object
        listOfChannels (list): list of channels

    Returns:
        bool: True if chat is not a channel or if it is not in the channel list
    """
    try:
        if chat.megagroup:
            print (f"{chat.title} is not a channel. Skipping...")
            return True
        elif chat.title not in listOfChannels:
            print (f"{chat.title} is not in the channel list. Skipping...")
            return True
    except AttributeError:
        print ("AttributeError")
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
    

def tryListOfChannels(listOfChannels:list) -> list:
    """
    Tries to grab a list of channels. If the file is not found, it raises an error.
    """
    try:
        listOfChannels = createListOfChannels()
    except FileNotFoundError:
        print(f"Error: No channel list found. Run the command -c or --channels to generate a channel list.")
        exit()
    except IOError as e:
        print(f"An error occurred: {str(e)}")
    return listOfChannels


def createConfig():
    """
    Asks the user for api_id, api_hash and username and writes them to a config file.
    """
    
    print("Please enter your api_id, api_hash and username. You can find them at https://my.telegram.org/apps")
    api = input("Enter your api_id: ")
    hash = input("Enter your api_hash: ")
    username = input("Enter your username: ")
    with open("config.ini", "w") as f:
        f.write("[Telegram]\n")
        f.write(f"api_id = {api}\n")
        f.write(f"api_hash = {hash}\n")
        f.write(f"username = {username}\n")
        
        
def getConfig()->tuple:
    """
    Reads the configuration file and returns the api_id, api_hash and username.
    """
    if not os.path.isfile("config.ini"):
        print("Config file not found. Creating config file...")
        createConfig()
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
    return api_id, api_hash, username


def channelVerif (result: object, listOfChannels: list) -> bool:
    """
    function to verify if the channels selected are correct
    
    Args:
        result: the result of GetDialogsRequest
        listOfChannels: list of channels
    Returns:
        bool: True if the user wants to exit
    """
    for chat in result.chats:
        if str(chat.title) in listOfChannels:
            print (chat.title)
        else:
            print (f"{chat.title} not selected")
    print ("-------------------------------------------------------------------------------")
    if input("These are the channels picked up by the script. Do you want to continue? (y/n)") == "n":
        return True
    return False