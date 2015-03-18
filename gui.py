#todo: when do I need root.mainloop()?

#Window process: main() makes one window, each function adds its own elements
#to the window on entry and wipes the window contents on exit/before calling
#the next function. Each window has its own nav button functions.

from tkinter import *
from tkinter import ttk

WIDTH = 600
HEIGHT = 450
MAIN_PAD = 10

def makeNavFrame(root, main, nextFun=None, backFun=None):
    '''Takes a root window, a Frame, and two button functions, sets up
    navigational buttons on the window, returns the containing frame. Only adds
    buttons if functions are given.'''

    NEXT_TEXT = 'Next -->'
    BACK_TEXT = '<-- Back'
    
    navFrame = ttk.Frame(root, padding=MAIN_PAD)
    navFrame.grid(row=1, column=0, sticky='sew')
    navFrame.columnconfigure(0, weight=1)
    navFrame.rowconfigure(0, weight=1)
    navFrame.rowconfigure(1, weight=1)

    if nextFun is not None:
        def forward():
            main.grid_remove()
            navFrame.destroy()
            nextFun(root)
        nextButton = ttk.Button(navFrame, text=NEXT_TEXT, command=forward)
        nextButton.grid(column=1, row=0, sticky='e')

    if backFun is not None:
        def back():
            main.grid_remove()
            navFrame.destroy()
            backFun(root)
        backButton = ttk.Button(navFrame, text=BACK_TEXT, command=back)
        backButton.grid(column=0, row=0, sticky='w')

    return navFrame

def main():
    '''Sets up the initial window.'''

    root = Tk()
    root.geometry('{}x{}'.format(WIDTH, HEIGHT))
    root.resizable(False, False)

    title(root)

    #root.after(100, title, root)
    #root.mainloop()

def title(root):
    '''Creates the title window.'''

    root.title("PokeBridge")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    try:
        root.titleFrame.grid(column=0, row=0, sticky='nsew')
        mainFrame = root.titleFrame
    except AttributeError:
        mainFrame = ttk.Frame(root, padding=MAIN_PAD)
        mainFrame.grid(column=0, row=0, sticky='nsew')
        for i in range(3):
            mainFrame.rowconfigure(i)
            mainFrame.columnconfigure(i)

        titleLabel = ttk.Label(mainFrame, text='PokeBridge')
        titleLabel.grid(column=1, row=0)

        bodyText = '''Hello, and welcome to PokeBridge! This simple application will allow you to transfer your Pok\u00E9mon from Generation II to Generation III, moving entire Boxes at a time. To get started, press the Next button.'''
        bodyLabel = ttk.Label(mainFrame, text=bodyText, justify='center',
                              wraplength=500)
        bodyLabel.grid(column=0, row=1, columnspan=3)

        pic1 = PhotoImage(file='res\\249.png')
        pic2 = PhotoImage(file='res\\250.png')
        pic1Label = ttk.Label(mainFrame, image=pic1)
        pic1Label.grid(column=0, row=0)
        pic2Label = ttk.Label(mainFrame, image=pic2)
        pic2Label.grid(column=2, row=0)
        mainFrame.pics = [pic1, pic2] #need this to avoid garbage collection...


        root.titleFrame = mainFrame

    navFrame = makeNavFrame(root, mainFrame, filePicker)

    root.mainloop()

def filePicker(root):
    '''Makes the window that lets the user specify save files and options.'''

    root.title("Select Save Files")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    try:
        root.filePickerFrame.grid(row=0, column=0, sticky='ns')
        mainFrame = root.filePickerFrame
    except AttributeError:
        mainFrame = ttk.Frame(root, padding=MAIN_PAD)
        mainFrame.grid(row=0, column=0, sticky='ns')
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)


        pickerFrame = ttk.Frame(mainFrame)
        pickerFrame.grid(row=0, column=0)

        pickText = "Select the Gen II save file to transfer Pok\u00E9mon from and the Gen III save file to transfer Pok\u00E9mon to."
        pickLabel = ttk.Label(pickerFrame, text=pickText)
        pickLabel.grid(row=0, column=0, columnspan=2, pady=10)

        fromButton = ttk.Button(pickerFrame, text='From...')
        fromButton.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        fromEntry = ttk.Entry(pickerFrame)
        fromEntry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        toButton = ttk.Button(pickerFrame, text='To...')
        toButton.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        toEntry = ttk.Entry(pickerFrame)
        toEntry.grid(row=2, column=1, sticky='w', padx=5, pady=5)


        optionFrame = ttk.Frame(mainFrame)
        optionFrame.grid(row=1, column=0)

        optionText = "Select the appropriate options from the drop-down menus below."
        optionLabel = ttk.Label(optionFrame, text=optionText)
        optionLabel.grid(row=0, column=0, columnspan=2, pady=10)

        gameChoices = ['Ruby', 'Sapphire', 'Emerald', 'FireRed', 'LeafGreen']
        langChoices = ['English', 'Japanese', 'French', 'Italian', 'German',
                       'Korean', 'Spanish']
        genderChoices = ['Male', 'Female']

        gameLabel = ttk.Label(optionFrame, text='Destination Game')
        gameLabel.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        gameCombo = ttk.Combobox(optionFrame, values=gameChoices)
        gameCombo.set(gameChoices[0])
        gameCombo.state(['readonly'])
        gameCombo.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        langLabel = ttk.Label(optionFrame, text='Game Language')
        langLabel.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        langCombo = ttk.Combobox(optionFrame, values=langChoices)
        langCombo.set(langChoices[0])
        langCombo.state(['readonly'])
        langCombo.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        genderLabel = ttk.Label(optionFrame, text='OT Gender')
        genderLabel.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        genderCombo = ttk.Combobox(optionFrame, values=genderChoices)
        genderCombo.set(genderChoices[0])
        genderCombo.state(['readonly'])
        genderCombo.grid(row=3, column=1, sticky='w', padx=5, pady=5)


        root.filePickerFrame = mainFrame


    navFrame = makeNavFrame(root, mainFrame, boxPicker, title)

    root.mainloop()

def boxPicker(root):
    '''Creates the window for selecting the boxes to be transferred.'''
    from pokeBridge import SaveGame
    numBoxes = SaveGame.NUMBER_OF_BOXES
    
    root.title("Box Selection")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    try:
        root.boxPickerFrame.grid(column=0, row=0, sticky='we')
        mainFrame = root.boxPickerFrame
    except AttributeError:
        mainFrame = ttk.Frame(root, padding=MAIN_PAD)
        mainFrame.grid(column=0, row=0, sticky='we')
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)


        boxesFrame = ttk.Frame(mainFrame)
        boxesFrame.grid(row=0, column=0, sticky='w')

        ttk.Label(boxesFrame, text='From').grid(row=0, column=0)
        ttk.Label(boxesFrame, text='To').grid(row=0, column=1)
        fromButtons = {}
        toCombos = {}
        comboTexts = {i:StringVar() for i in range(numBoxes)}
        #todo: get actual box names
        toChoices = ["None"] + ["BOX {}".format(i+1) for i in range(numBoxes)]
        for i in range(numBoxes):
            #todo: get actual box names
            fromButtons[i] = ttk.Button(boxesFrame, text="BOX {}".format(i+1))
            fromButtons[i].grid(row=i+1, column=0, padx=5)
            toCombos[i] = ttk.Combobox(boxesFrame, values=toChoices, width=10,
                                      textvariable=comboTexts[i])
            toCombos[i].grid(row=i+1, column=1, padx=5)
            toCombos[i].set(toChoices[0])
            toCombos[i].state(['readonly'])
        #todo: make buttons do things

        
        displayFrame = ttk.Frame(mainFrame)
        displayFrame.grid(row=0, column=1, sticky='e')
        DISP_WIDTH = 350

        instructs = 'Use the drop-down menus under the "To" column to choose where the Pok\u00E9mon in the corresponding "From" box will be sent. Boxes marked with "None" will not be transferred. Click the name of the From box to see its contents in the display below.'
        instrLabel = ttk.Label(displayFrame, text=instructs,
                               wraplength=DISP_WIDTH)
        instrLabel.grid(row=0, column=0)
        #todo: make text of labelframe variable with what box it's showing
        boxDisplay = ttk.Labelframe(displayFrame, text='Old Box Contents')
        boxDisplay.grid(row=1, column=0, padx=5, pady=20)
        pic = PhotoImage(file="res\\000.png")
        for i in range(5):
            for j in range(4):
                ttk.Label(boxDisplay, image=pic).grid(column=i, row=j)
        #todo: make warning red
        warning = "WARNING! Any Pok\u00E9mon that previously inhabited chosen boxes in the Gen III save file will be ERASED. It is recommended that you only select empty Gen III boxes."
        warningLabel = ttk.Label(displayFrame, text=warning,
                                 wraplength=DISP_WIDTH)
        warningLabel.grid(row=2, column=0)


        root.boxPickerFrame = mainFrame


    navFrame = makeNavFrame(root, mainFrame, overwritePicker, filePicker)

    root.mainloop()

def overwritePicker(root):
    '''Creates the window for deciding to overwrite or not.'''

    root.title("Overwrite?")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    try:
        root.overwritePickerFrame.grid(row=0, column=0)
        mainFrame = root.overwritePickerFrame
    except AttributeError:
        mainFrame = ttk.Frame(root, padding=MAIN_PAD)
        mainFrame.grid(row=0, column=0)

        choice = BooleanVar(value=True)
        choice1Radio = ttk.Radiobutton(mainFrame, text='Overwrite', variable=choice,
                                  value=True)
        choice1Radio.grid(row=0, column=0, sticky='w')
        choice2Radio = ttk.Radiobutton(mainFrame, text='Do not overwrite',
                                   variable=choice, value=False)
        choice2Radio.grid(row=1, column=0, sticky='w')


        pickerFrame = ttk.Frame(mainFrame)
        pickerFrame.grid(row=2, column=0)

        gen2Label = ttk.Label(pickerFrame, text='New Gen II file:')
        gen2Label.grid(row=0, column=0, columnspan=2)
        gen2Button = ttk.Button(pickerFrame, text='To...')
        gen2Button.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        gen2Entry = ttk.Entry(pickerFrame)
        gen2Entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        gen3Label = ttk.Label(pickerFrame, text='New Gen III file:')
        gen3Label.grid(row=2, column=0, columnspan=2)
        gen3Button = ttk.Button(pickerFrame, text='To...')
        gen3Button.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        gen3Entry = ttk.Entry(pickerFrame)
        gen3Entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)


        root.overwritePickerFrame = mainFrame


    navFrame = makeNavFrame(root, mainFrame, None, boxPicker) #todo: fwd

    root.mainloop()    

def nameHandler(name, message):
    '''Takes a string name and character, provides an interface for correcting
    the illegal name, returns a new legal string name.'''

    def end(*args):
        if len(newname.get()) > 0:
            root.destroy()

    root = Tk() #todo: this might have to change
    root.title("Bad Name")
    root.resizable(False, False)

    mainFrame = ttk.Frame(root, padding=MAIN_PAD)
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



if __name__ == '__main__':
    main()
