import re
def parseReactions(text):
    pattern = r'count=\D*(\d+)'  # Regular expression pattern to match numbers after "count=15"
    numbers = re.findall(pattern, text)
    total_sum = sum(map(int, numbers))
    return total_sum

#def parseDate():
    
    
