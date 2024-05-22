# import only asksaveasfile from filedialog 
# which is used to save file in any extension 
from tkinter.filedialog import asksaveasfilename


# function to call when user press 
# the save button, a filedialog will 
# open and ask to save file 
def save(): 
    files = [('CSV file', '*.csv*')]  
    file = asksaveasfilename(filetypes = files, defaultextension = files)
    return file
