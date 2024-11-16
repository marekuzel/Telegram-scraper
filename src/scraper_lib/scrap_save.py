import csv
import re



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