import csv
import re
import pandas as pd



def saveComplex(simpleData:bool, d:dict):
    if simpleData:
        simpleCsvWriter(d)

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


def getMessageLink(chat_id: int, message_id: int) -> str:
    """Returns the link to a message.

    Args:
        chat_id (int): chat_id
        message_id (int): message_id

    Returns:
        str: link to the message
    """
    base_url = "https://t.me/c/"
    return f"{base_url}{chat_id}/{message_id}"
            

def formatMessage(message: str, client)->list:
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
    list.append(getMessageLink(message.chat.id, message.id))
    try:
        list.append((client.get_entity(message.fwd_from.from_id)).username)
    except:
        list.append("None")
    return list

def collectData(chatId, client, startDate, endDate) -> pd.DataFrame:
    # Initialize a dictionary with empty lists for each column
    data = {
        "Id": [],
        "msg_title": [],
        "reactions": [],
        "views": [],
        "date": [],
        "messageBody": [],
        "link": [],
        "fwdFrom": [],
        "replies": [],
        "forwards": [],
        "postAuthor": [],
        "embededURL": []
    }
    for message in client.iter_messages(chatId):
        try:
            if message.date.replace(tzinfo=None) > endDate:
                continue
            elif message.date.replace(tzinfo=None) < startDate:
                break
            
            # Populate each column list with data for this message
            data["Id"].append(message.id)
            data["msg_title"].append(" ".join(str(message.text).split(" ")[:4]) if message.text else "NULL")
            data["reactions"].append(parseReactions(str(message.reactions)))
            data["views"].append(message.views)
            data["date"].append(str(message.date.replace(tzinfo=None)))
            data["messageBody"].append(message.text if message.text else "NULL")
            data["link"].append(getMessageLink(message.chat.id, message.id))
            data["fwdFrom"].append(message.forwarded_from if message.forwarded_from else "NULL")
            data["replies"].append(message.replies if message.replies else "NULL")
            data["forwards"].append(message.forwards if message.forwards else "NULL")
            data["postAuthor"].append(message.sender.username if message.sender else "NULL")
            data["embededURL"].append(message.web_preview.url if message.web_preview else "NULL")
        except:
            pass
    for i in data:
        print (data[i])
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)
    return df

def extFormatMessage(dataList, message):
    dataList[0].append(message.Id)
    dataList[1].append (" ".join(str(message.text).split(" ")[:4]))
    dataList[2] = message.sender.username
    list.append(msg_title)
    list.append(parseReactions(str(message.reactions)))
    list.append(message.views)
    list.append(str(message.date.replace(tzinfo=None)))
    list.append(message.text)
    list.append(getMessageLink(message.chat.id, message.id))
    
    
def simpleCsvWriter(d:dict):
    """
    Writes the less extensive data to a csv file
    """

    with open("data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        listOfHeadings = ["Author", "Title", "Interactions", "Views", "Date", "Message body", "Link", "Forward from"]

        writer.writerow(listOfHeadings)
        for line in d.values():
            writer.writerow(line)