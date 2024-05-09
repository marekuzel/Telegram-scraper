from fuzzywuzzy import fuzz


def getListOfSubjects(File:str) -> dict:
    """creates list of names of the subjects to count from the text file

    Args:
        File (str): name of the text file

    Returns:
        list: list of subjects
    """
    subjects = []
    try:
        with open(File, "r") as f:
            listOfSubjects = f.readlines()
    except:
        print(f"Error: No subjects.txt found in working directory. Create a text file with one name/subject on each line")
        exit()
    for line in listOfSubjects:
        line = line.strip()
        line = line.lower()
        subjects.append(line)
    return subjects


def name_create(text:str) -> dict:
    """counts number of subjects in the given text

    Args:
        text (str): text body of the message
    Returns:
        dict: dictionary of subjects and their count
    """
    subjects = getListOfSubjects("subjects.txt")
    subjectsD = {}
    for name in subjects:
        subjectsD[name] = 0
    SIMILARITY_THRESHOLD=70 #this seemed to work fine for me, however, this feature is very unreliable and should be used only for estimates
    textList = text.lower().split()
    for subject in subjects:
        for word in textList:
            similarity = fuzz.ratio(subject, word)
            if similarity >= SIMILARITY_THRESHOLD:
                subjectsD[subject] += 1
                with open("spravy.txt", "a") as w:
                    w.write(text)
                    w.write("\n-----------------------\n")
    return subjectsD


def name_countMentions(message:str, subjects:dict)->dict:
    """
    Takes a message and counts the number of mentions of each subject in the message
    Args: 
        message (str): message.text
        subjects (dict): Dictionary storing appearances of each subject
    Returns:
        dict: dictionary of subjects and their count
    """
    subjectsPerMessage = name_create(message)
    for name in subjectsPerMessage:
        if name not in subjects:
            subjects[name] = subjectsPerMessage[name]
        else:
            subjects[name] += subjectsPerMessage[name]
    return subjects