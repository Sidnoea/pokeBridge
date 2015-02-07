#todo: everything lol

#Window process: main() makes one window, each function adds its own elements
#to the window on entry and wipes the window contents on exit/before calling
#the next function.

from tkinter import *
from tkinter import ttk

WIDTH = 600
HEIGHT = 400
NEXT_TEXT = 'Next -->'
BACK_TEXT = '<-- Back'

def main():
    '''Sets up the initial window.'''

    root = Tk()
    root.geometry('{}x{}'.format(WIDTH, HEIGHT))
    root.resizable(False, False)

    root.after(100, title, root)
    root.mainloop()

def boxPicker(root):
    '''Creates the window for selecting the boxes to be transferred.'''
    from pokeBridge import SaveGame
    numBoxes = SaveGame.NUMBER_OF_BOXES

    def back(): #todo: write this
        '''Goes to the previous page.'''

        mainFrame.destroy()
        filePicker(root)

    def forward(): #todo: write this
        '''Goes to the next page.'''

        pass

    def updateBoxes():
        '''Toggles the lists of new boxes based on the checkbox statuses.'''
        
        for i in range(numBoxes):
            box = comboboxes[i+1]
            if checks[i+1].get():
                box.state(['!disabled'])
            else:
                box.state(['disabled'])
        #todo: update box display
    
    root.title("Box Selection")

    mainFrame = ttk.Frame(root, padding=3)
    mainFrame.grid(column=0, row=0)
##    for i in [1,2]:
##        mainFrame.columnconfigure(i, minsize=WIDTH/3)

    Label(mainFrame, text='Old Box').grid(row=0, column=0, columnspan=2)
    Label(mainFrame, text='New Box').grid(row=0, column=3, columnspan=2)

    boxNames = ["BOX {}".format(i+1) for i in range(numBoxes)]
    checkbuttons = {}
    checks = {}
    comboboxes = {}
    combotexts = {}
    
    for i in range(numBoxes):
        #add checkboxes
        checks[i+1] = BooleanVar(value=0)
        b = ttk.Checkbutton(mainFrame, text=boxNames[i], variable=checks[i+1],
                            command=updateBoxes)
        b.grid(column=0 if i+1 <= numBoxes/2 else 1,
               row=int(i%(numBoxes/2) + 1))
        checkbuttons[i+1] = b
        
        #add lists
        combotexts[i+1] = StringVar()
        c = ttk.Combobox(mainFrame, values=boxNames, width=7,
                         textvariable=combotexts[i+1])
        c.set(boxNames[i])
        c.grid(column=3 if i+1 <= numBoxes/2 else 4,
               row=int(i%(numBoxes/2) + 1), pady=1)
        c.state(['readonly', 'disabled'])
        comboboxes[i+1] = c

    boxDisplay = ttk.Labelframe(mainFrame, text='Old Box Contents')
    boxDisplay.grid(row=1, column=2, rowspan=numBoxes, padx=5)
    pic = PhotoImage(file="res\\000.png")
    for i in range(5):
        for j in range(4):
            ttk.Label(boxDisplay, image=pic).grid(column=i, row=j)

    backButton = ttk.Button(mainFrame, text=BACK_TEXT, command=back)
    backButton.grid(column=0, row=numBoxes+2, pady=5)

    nextButton = ttk.Button(mainFrame, text=NEXT_TEXT, command=forward)
    nextButton.grid(column=4, row=numBoxes+2, pady=5)

    root.mainloop()

def filePicker(root):
    '''Makes the window that lets the user specify save files.'''

    def back():
        '''Goes to the previous page.'''

        mainFrame.destroy()
        title(root)

    def forward():
        '''Goes to the next page.'''

        mainFrame.destroy()
        boxPicker(root)

    root.title("Select Save Files")

    mainFrame = ttk.Frame(root, padding=3)
    mainFrame.grid(column=0, row=0, sticky='nsew')
    for i in range(3):
        mainFrame.rowconfigure(i, minsize=HEIGHT/3)
        mainFrame.columnconfigure(i, minsize=WIDTH/3)

    temp = ttk.Label(mainFrame, text='placeholder')
    temp.grid(column=1, row=1)

    backButton = ttk.Button(mainFrame, text=BACK_TEXT, command=back)
    backButton.grid(column=0, row=2, pady=5)

    nextButton = ttk.Button(mainFrame, text=NEXT_TEXT, command=forward)
    nextButton.grid(column=2, row=2, pady=5)

def nameHandler(name, message):
    '''Takes a string name and character, provides an interface for correcting
    the illegal name, returns a new legal string name.'''

    def end(*args):
        if len(newname.get()) > 0:
            root.destroy()

    root = Tk() #todo: this might have to change
    root.title("Bad Name")
    root.resizable(False, False)

    mainFrame = ttk.Frame(root, padding=3)
    mainFrame.grid(column=0, row=0, sticky='nwes')

    newname = StringVar()
    newname.set(name)

    nameEntry = ttk.Entry(mainFrame, textvariable=newname)
    nameEntry.grid(row=1, sticky='we')

    ttk.Label(mainFrame, text=message).grid(row=0)

    for child in mainFrame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    nameEntry.focus()
    root.bind('<Return>', end)

    #todo: disable the ability to close the window instead? add abort option?
    if len(newname.get()) < 1:
        return nameHandler(name, message)
    else:
        return newname.get()

def title(root):
    '''Creates the title window.'''

    def back():
        '''Goes to the previous page.'''

        pass

    def forward():
        '''Goes to the next page.'''

        mainFrame.destroy()
        filePicker(root)

    BODY_TEXT = '''Hello, and welcome to PokeBridge! This simple application will allow you to transfer your Pok\u00E9mon from Generation II to Generation III, moving entire Boxes at a time. To get started, press the Next button.'''

    root.title("PokeBridge")

    mainFrame = ttk.Frame(root, padding=3)
    mainFrame.grid(column=0, row=0, sticky='nsew')
    for i in range(3):
        mainFrame.rowconfigure(i, minsize=HEIGHT/3)
        mainFrame.columnconfigure(i, minsize=WIDTH/3)

    titleLabel = ttk.Label(mainFrame, text='PokeBridge')
    titleLabel.grid(column=1, row=0)

    bodyLabel = ttk.Label(mainFrame, text=BODY_TEXT, justify='center',
                          wraplength=500)
    bodyLabel.grid(column=0, row=1, columnspan=3)

    pic1 = PhotoImage(file='res\\249.png')
    pic2 = PhotoImage(file='res\\250.png')
    pic1Label = ttk.Label(mainFrame, image=pic1)
    pic1Label.grid(column=0, row=0)
    pic2Label = ttk.Label(mainFrame, image=pic2)
    pic2Label.grid(column=2, row=0)
    mainFrame.pics = [pic1, pic2] #need this to avoid garbage collection...

    nextButton = ttk.Button(mainFrame, text=NEXT_TEXT, command=forward)
    nextButton.grid(column=2, row=2)

if __name__ == '__main__':
    main()
