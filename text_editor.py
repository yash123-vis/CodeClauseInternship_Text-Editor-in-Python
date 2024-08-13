# Importing
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import datetime
import os
import keyword

# Creating and initializing the window
root = Tk()
root.title("NText")
root.geometry("600x400")  # Adjusted for better visibility
root.resizable(height=None, width=None)

# *****Status bar*****
statbarb = Label(root, text="Ln", relief=SUNKEN, bd=1, anchor="w")
statbarb.pack(side=BOTTOM, fill=X)

# *****Global variables*****

# Variable for the present file loaded
filvar = None

# *****Text Area Frame*****

frame = Frame(root)
frame.pack(fill=BOTH, expand=1)

# Adding the text area
textarea = Text(frame, undo=True, wrap=None)
textarea.pack(side=LEFT, fill=BOTH, expand=1)

# *****Scroll Bar******
# Creating the vertical scrollbar
scrollbarv = Scrollbar(frame, command=textarea.yview)
# Adding the scrollbar to the text area
textarea.config(yscrollcommand=scrollbarv.set)
# Packing the scrollbar
scrollbarv.pack(side=RIGHT, fill=Y)

# *****Syntax Highlighting*****
def syntax_highlight(event=None):
    textarea.tag_remove("keyword", "1.0", "end")
    
    keywords = keyword.kwlist
    for kw in keywords:
        start = "1.0"
        while True:
            start = textarea.search(r'\b' + kw + r'\b', start, stopindex=END)
            if not start:
                break
            end = f"{start}+{len(kw)}c"
            textarea.tag_add("keyword", start, end)
            start = end
            textarea.tag_config("keyword", foreground="blue")

textarea.bind("<KeyRelease>", syntax_highlight)

# *****Various functions of the text editor
def createnew(*args):
    global root, textarea, filvar
    filvar = None
    root.title("New File")
    textarea.delete(1.0, END)

def openfile(*args):
    global root, textarea, filvar, origfilecontents
    filvar = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
    if filvar == "":
        filvar = None
        origfilecontents = None
    else:
        try:
            root.title(os.path.basename(filvar))
            textarea.delete(1.0, END)
            with open(filvar, "r") as file:
                textarea.insert(1.0, file.read())
            origfilecontents = textarea.get(1.0, END)
        except Exception as e:
            root.title("NText")
            showerror("ERROR", f"Unable to open {filvar}\nNot a .txt file!\n{str(e)}")

def savefile(*args):
    global root, textarea, filvar, origfilecontents
    if filvar is None:
        saveasfile()
    else:
        with open(filvar, "w") as file:
            origfilecontents = textarea.get(1.0, END)
            file.write(textarea.get(1.0, END))
        showinfo("Successfully saved", "All changes saved")

def saveasfile():
    global root, textarea, filvar
    filvar = asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if filvar == "":
        filvar = None
    else:
        with open(filvar, "w") as file:
            file.write(textarea.get(1.0, END))
        showinfo("Successfully saved", f"Saved as {filvar} successfully!")

def datetimefunc(*args):
    global textarea
    textarea.insert(END, str(datetime.datetime.now()))

def cutop():
    global textarea
    textarea.event_generate("<<Cut>>")

def copyop():
    global textarea
    textarea.event_generate("<<Copy>>")

def pasteop():
    global textarea
    textarea.event_generate("<<Paste>>")

def deleteop():
    global textarea
    ranges = textarea.tag_ranges(SEL)
    textarea.delete(*ranges)

def about():
    showinfo("About NText", "This is a text editor built using Tkinter\nDeveloped by Neeramitra Reddy\nGithub: https://github.com/neeru1207")

def exitapplication():
    root.quit()

def selectall():
    global textarea
    textarea.event_generate("<<SelectAll>>")

def undofunc():
    global textarea
    try:
        textarea.edit_undo()
    except:
        pass

def redofunc():
    global textarea
    try:
        textarea.edit_redo()
    except:
        pass

def findlinecount():
    global textarea, submenu3
    if textarea.compare("end-1c", "!=", "1.0"):
        submenu6.entryconfig(0, label=str(f"{int(textarea.index('end').split('.')[0]) - 1} Lines"))

def findwordcount():
    global textarea, submenu5
    if textarea.compare("end-1c", "!=", "1.0"):
        submenu5.entryconfig(0, label=str(f"{len(textarea.get(0.0, END).replace('\n', ' ').split(' ')) - 1} Words"))

def exitwithoutsaving():
    global root, textarea, origfilecontents
    if filvar is not None and origfilecontents != textarea.get(1.0, END):
        result = askquestion(title="Exit", message=f"Do you want to save changes made to {(os.path.basename(filvar) if filvar is not None else 'New File')} ?", icon='warning')
        if result == 'yes':
            savefile()
        else:
            exitapplication()
    else:
        exitapplication()

# *****Binding shortcut keys to functions*****

textarea.bind("<F5>", datetimefunc)
textarea.bind("<Control-n>", createnew)
textarea.bind("<Control-s>", savefile)
textarea.bind("<Control-o>", openfile)

# *****Adding the menus*****
menu = Menu(root)
root.config(menu=menu)

# Adding the File submenu
submenu1 = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=submenu1)
submenu1.add_command(label="New    Ctrl+N", command=createnew)
submenu1.add_command(label="Open   Ctrl+O", command=openfile)
submenu1.add_command(label="Save    Ctrl+S", command=savefile)
submenu1.add_command(label="Save as", command=saveasfile)
submenu1.add_separator()
submenu1.add_command(label="Exit", command=exitwithoutsaving)

# Adding the Edit submenu
submenu2 = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=submenu2)
submenu2.add_command(label="Undo        Ctrl+Z", command=undofunc)
submenu2.add_command(label="Redo        Ctrl+Y", command=redofunc)
submenu2.add_separator()
submenu2.add_command(label="Cut          Ctrl+X", command=cutop)
submenu2.add_command(label="Copy       Ctrl+C", command=copyop)
submenu2.add_command(label="Paste       Ctrl+V", command=pasteop)
submenu2.add_command(label="Delete      Del", command=deleteop)
submenu2.add_separator()
submenu2.add_command(label="Select all    Ctrl+A", command=selectall)
submenu2.add_command(label="Date/Time   F5", command=datetimefunc)

# Adding the view submenu
submenu3 = Menu(menu, tearoff=0)
submenu5 = Menu(submenu3, tearoff=0, postcommand=findwordcount)
submenu6 = Menu(submenu3, tearoff=0, postcommand=findlinecount)
menu.add_cascade(label="View", menu=submenu3)
submenu3.add_cascade(label="Word Count", menu=submenu5)
submenu3.add_cascade(label="Line Count", menu=submenu6)
submenu5.add_command(label="0 Words", command=None)
submenu6.add_command(label="0 Lines", command=None)

# Adding the about submenu
submenu4 = Menu(menu, tearoff=0)
menu.add_command(label="About", command=about)

root.mainloop()
