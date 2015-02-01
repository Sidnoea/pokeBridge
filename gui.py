from tkinter import *
from tkinter import ttk

def boxSelect():
    from pokeBridge import SaveGame
    numBoxes = SaveGame.NUMBER_OF_BOXES

    def back(): #todo: write this
        '''Goes to the previous page.'''

        pass

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
    
    root = Tk()
    root.title("Box Selection")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe = ttk.Frame(root, padding=5)
    mainframe.grid(column=0, row=0, sticky='nsew')
    for i in range(numBoxes+1):
        mainframe.rowconfigure(i, weight=1)
    for i in range(3):
        mainframe.columnconfigure(i, weight=1)

    Label(mainframe, text='Old Box').grid(row=0, column=0)
    Label(mainframe, text='Old Box Content').grid(row=0, column=1)
    Label(mainframe, text='New Box').grid(row=0, column=2)

    boxNames = ["BOX {}".format(i+1) for i in range(numBoxes)]
    checkbuttons = {}
    checks = {}
    comboboxes = {}
    combotexts = {}
    
    for i in range(numBoxes):
        #add checkboxes
        checks[i+1] = BooleanVar(value=0)
        b = ttk.Checkbutton(mainframe, text=boxNames[i], variable=checks[i+1],
                            command=updateBoxes)
        b.grid(column=0, row=i+1)
        checkbuttons[i+1] = b
        
        #add lists
        combotexts[i+1] = StringVar()
        c = ttk.Combobox(mainframe, values=boxNames, width=7,
                         textvariable=combotexts[i+1])
        c.set(boxNames[i])
        c.grid(column=2, row=i+1, pady=1)
        c.state(['readonly', 'disabled'])
        comboboxes[i+1] = c

    boxDisplay = ttk.Frame(mainframe, relief='sunken', borderwidth=10)
    boxDisplay.grid(row=1, column=1, rowspan=numBoxes, padx=5)
    pic = PhotoImage(file="res\\000.png")
    for i in range(5):
        for j in range(4):
            ttk.Label(boxDisplay, image=pic).grid(column=i, row=j)

    backButton = ttk.Button(mainframe, text='<-- Back', command=back)
    backButton.grid(row=numBoxes+2, column=0, pady=5)

    nextButton = ttk.Button(mainframe, text='Next -->', command=forward)
    nextButton.grid(row=numBoxes+2, column=2, pady=5)

    root.mainloop()

def nameHandler(name, message):
    '''Takes a string name and character, provides an interface for correcting
    the illegal name, returns a new legal string name.'''

    def end(*args):
        if len(newname.get()) > 0:
            root.destroy()

    root = Tk()
    root.title("Bad Name")
    root.resizable(0,0)

    mainframe = ttk.Frame(root, padding=3)
    mainframe.grid(column=0, row=0, sticky='nwes')

    newname = StringVar()
    newname.set(name)

    nameEntry = ttk.Entry(mainframe, textvariable=newname)
    nameEntry.grid(row=1, sticky='we')

    ttk.Label(mainframe, text=message).grid(row=0)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    nameEntry.focus()
    root.bind('<Return>', end)

    root.mainloop()

    #todo: disable the ability to close the window instead? add abort option?
    if len(newname.get()) < 1:
        return nameHandler(name, message)
    else:
        return newname.get()

if __name__ == '__main__':
    boxSelect()
