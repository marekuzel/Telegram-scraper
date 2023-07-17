import re
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
    list.append(str(message.date))
    list.append(message.text)
    list.append(get_message_link(message.chat.id, message.id))
    return list