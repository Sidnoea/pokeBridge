#todo: Spawn a window when things go wrong, so end-users can file bug reports.
#todo: If all the window functions return the same grid configs, then just omit
#      that return piece and handle it in the Root.
#todo: Test overwrite mode.

#Window process: main makes one Root, which changes content by removing the
#current content and replacing it with the Frame generated by the functions
#passed to it. Each Frame should have its own Nav for navigation buttons.

debug = False

from tkinter import BooleanVar, PhotoImage, StringVar, Tk, Toplevel
from tkinter import filedialog, ttk

WIDTH = 600
HEIGHT = 450
MAIN_PAD = 10

#globals for passing to transfer function
oldGen2 = ''
newGen2 = ''
oldGen3 = ''
newGen3 = ''
oldBoxNums = []
newBoxNums = []
newGame = ''
language = ''
gender = ''


class Root(Tk):
    '''A class for the root window of the GUI. Takes a list of page functions.
    Each page function should take a root Frame and return a list containing a
    Frame, a string page title, and a dictionary of grid configuration
    options.'''

    def __init__(self, pageFuns):
        from os import getcwd

        super().__init__()
        
        self.pageFuns = pageFuns

        self.page = 0
        self.lastPage = len(pageFuns) - 1
        self.pages = {}
        self.titles = {}
        self.dir = getcwd() #todo: make this global?
        self.boxes = [] #todo: put this somewhere else?

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.mainFrame = ttk.Frame()
        self.load(0)

    def load(self, page):
        '''Takes an int page number, loads that page.'''

        self.mainFrame.grid_remove()
        self.page = page

        if page in self.pages:
            self.mainFrame = self.pages[page]
            self.mainFrame.grid()
            self.title(self.titles[page])
        else:
            newFrame, title, config = self.pageFuns[page](self)
            newFrame.grid(row=0, column=0, cnf=config)
            self.pages[page] = newFrame
            self.mainFrame = newFrame
            self.title(title)
            self.titles[page] = title

    def nextPage(self):
        '''Loads the next page.'''

        if self.page < self.lastPage:
            self.load(self.page + 1)

    def prevPage(self):
        '''Loads the previous page.'''

        if self.page > 0:
            self.load(self.page - 1)

class Nav(ttk.Frame):
    '''A class for navigational Frames. Takes a master Frame and two
    navigational functions.'''

    def __init__(self, master, backFun, nextFun):
        super().__init__(master, padding=MAIN_PAD)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        backButton = ttk.Button(self, text='<-- Back', command=backFun)
        backButton.grid(row=0, column=0, sticky='w')
        self.backButton = backButton

        nextButton = ttk.Button(self, text='Next -->', command=nextFun)
        nextButton.grid(row=0, column=1, sticky='e')
        self.nextButton = nextButton

    def disable(self, direction, boolean):
        '''Takes a string 'back' or 'next' and a bool, disables the Button if
        boolean is True, enables it if boolean is False.'''

        button = getattr(self, direction + 'Button')
        if boolean:
            button.state(['disabled'])
        else:
            button.state(['!disabled'])
    
    def hide(self, direction, boolean):
        '''Takes a string 'back' or 'next' and a bool, hides the Button if
        boolean is True, unhides it if boolean is False.'''

        button = getattr(self, direction + 'Button')
        if boolean:
            button.grid_remove()
        else:
            button.grid()

def getDir(fileName):
    '''Takes a string file name, returns the string directory of that file.'''

    i = fileName.rfind('\\')
    if i == -1:
        return fileName[:fileName.rfind('/')]
    else:
        return fileName[:i]

#todo: get rid of this if you don't end up using it semi-frequently
def setState(boolean, state, widgets):
    '''Takes a bool, a string, and a list of widgets, enables the state for
    each widget if the bool is True, disables the state if False.'''

    if boolean:
        for w in widgets:
            w.state([state])
    else:
        for w in widgets:
            w.state(['!'+state])

def main():
    '''Sets up the initial window, runs the program.'''

    root = Root([titleWindow, fileWindow, boxWindow, overwriteWindow,
                 confirmWindow, transferWindow, doneWindow])
    root.geometry('{}x{}'.format(WIDTH, HEIGHT))
    root.resizable(False, False)

    root.mainloop()

def titleWindow(root):
    '''Creates the title window.'''

    baseFrame = ttk.Frame(root)
    baseFrame.rowconfigure(0, weight=1)
    baseFrame.columnconfigure(0, weight=1)

    
    mainFrame = ttk.Frame(baseFrame, padding=MAIN_PAD)
    mainFrame.grid(row=0, column=0, sticky='n')

    titleLabel = ttk.Label(mainFrame, text='Pok\u00E9Bridge')
    titleLabel.grid(row=0, column=1)

    bodyText = '''Hello, and welcome to Pok\u00E9Bridge! This simple application will allow you to transfer your Pok\u00E9mon from Generation II to Generation III, moving entire Boxes at a time. To get started, press the Next button.'''
    bodyLabel = ttk.Label(mainFrame, text=bodyText, justify='center',
                          wraplength=500)
    bodyLabel.grid(row=1, column=0, columnspan=3)

    pic1 = PhotoImage(file='res/old025.gif')
    pic1Label = ttk.Label(mainFrame, image=pic1)
    pic1Label.grid(row=0, column=0)

    pic2 = PhotoImage(file='res/025.gif')
    pic2Label = ttk.Label(mainFrame, image=pic2)
    pic2Label.grid(row=0, column=2)
    
    mainFrame.pics = [pic1, pic2] #avoiding garbage collection


    navFrame = Nav(baseFrame, root.prevPage, root.nextPage)
    navFrame.grid(row=1, column=0, sticky='we')
    navFrame.hide('back', True)

    return (baseFrame, 'Pok\u00E9Bridge', {'sticky':'nsew'})

def fileWindow(root):
    '''Makes the window that lets the user specify save files and options.'''

    def nextPage():
        global oldGen2, oldGen3, newGame, language, gender

        oldGen2 = fromText.get()
        oldGen3 = toText.get()
        newGame = gameCombo.get()
        language = langCombo.get()
        gender = genderCombo.get()

        with open(oldGen2, 'br') as file:
            root.boxes = getBoxes(file.read())

        root.nextPage()

    def nextToggle(*args):
        if fromText.get() == '' or toText.get() == '':
            navFrame.disable('next', True)
        else:
            navFrame.disable('next', False)

    def fromDialog():
        askOpen = filedialog.askopenfilename
        file = askOpen(title='Gen II Save File', initialdir=root.dir,
                       filetypes=[('GB Save', '.sav'), ('All Files', '.*')])
        if file != '':
            fromText.set(file)
            fromEntry.after_idle(fromEntry.xview_moveto, 1)
            root.dir = getDir(file)
    
    def toDialog():
        askOpen = filedialog.askopenfilename
        file = askOpen(title='Gen III Save File', initialdir=root.dir,
                       filetypes=[('GBA Save', '.sav'), ('All Files', '.*')])
        if file != '':
            toText.set(file)
            toEntry.after_idle(toEntry.xview_moveto, 1)
            root.dir = getDir(file)

    def getBoxes(data):
        from pokeBridge import Box, OldSaveFile

        boxes = []
        for offset in OldSaveFile.BOX_OFFSETS:
            box = []
            count = data[offset]
            for i in range(count):
                box.append(data[offset + 1 + i])
            for i in range(Box.OLD_SIZE - len(box)): #pad with 0
                box.append(0x0)
            boxes.append(box)

        return boxes

    baseFrame = ttk.Frame(root)
    baseFrame.rowconfigure(0, weight=1)
    baseFrame.columnconfigure(0, weight=1)
    
    
    mainFrame = ttk.Frame(baseFrame, padding=MAIN_PAD)
    mainFrame.grid(row=0, column=0)
    mainFrame.rowconfigure(0, weight=1)
    mainFrame.columnconfigure(0, weight=1)
    

    pickerFrame = ttk.Frame(mainFrame)
    pickerFrame.grid(row=0, column=0, sticky='s')

    pickText = "Select the Gen II save file to transfer Pok\u00E9mon from and the Gen III save file to transfer Pok\u00E9mon to."
    pickLabel = ttk.Label(pickerFrame, text=pickText, wraplength=WIDTH-50,
                          justify='center')
    pickLabel.grid(row=0, column=0, columnspan=2, pady=10)

    fromButton = ttk.Button(pickerFrame, text='From...', command=fromDialog)
    fromButton.grid(row=1, column=0, sticky='e', padx=5, pady=5)

    fromText = StringVar()
    fromText.trace('w', nextToggle)
    fromEntry = ttk.Entry(pickerFrame, textvariable=fromText, state='readonly')
    fromEntry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
    
    toButton = ttk.Button(pickerFrame, text='To...', command=toDialog)
    toButton.grid(row=2, column=0, sticky='e', padx=5, pady=5)

    toText = StringVar()
    toText.trace('w', nextToggle)
    toEntry = ttk.Entry(pickerFrame, textvariable=toText, state='readonly')
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
    
    gameCombo = ttk.Combobox(optionFrame, values=gameChoices,
                             state='readonly')
    gameCombo.set(gameChoices[0])
    gameCombo.grid(row=1, column=1, sticky='w', padx=5, pady=5)
    
    langLabel = ttk.Label(optionFrame, text='Game Language')
    langLabel.grid(row=2, column=0, sticky='e', padx=5, pady=5)
    
    langCombo = ttk.Combobox(optionFrame, values=langChoices,
                             state='readonly')
    langCombo.set(langChoices[0])
    langCombo.grid(row=2, column=1, sticky='w', padx=5, pady=5)
    
    genderLabel = ttk.Label(optionFrame, text='OT Gender')
    genderLabel.grid(row=3, column=0, sticky='e', padx=5, pady=5)
    
    genderCombo = ttk.Combobox(optionFrame, values=genderChoices,
                               state='readonly')
    genderCombo.set(genderChoices[0])
    genderCombo.grid(row=3, column=1, sticky='w', padx=5, pady=5)


    navFrame = Nav(baseFrame, root.prevPage, nextPage)
    navFrame.grid(row=1, column=0, sticky='we')

    if debug:
        fromText.set('C:/Users/Sidnoea/Documents/GitHub/pokeBridge/Old Gen 2.sav')
        toText.set('C:/Users/Sidnoea/Documents/GitHub/pokeBridge/Old Gen 3.sav')

    nextToggle()

    return (baseFrame, 'Select Save Files', {'sticky':'nsew'})

def boxWindow(root):
    '''Creates the window for selecting the boxes to be transferred.'''
    from pokeBridge import Box, SaveGame
    from pokeBridge import oldNameTrans
    global oldGen2

    boxLen = Box.OLD_SIZE
    numBoxes = SaveGame.NUMBER_OF_BOXES

    def makeButtonFun(i):
        def buttonFun():
            boxDisplay['text'] = comboChoices[i+1]
            boxPics = []
            boxIDs = root.boxes[i]
            for j in range(boxLen):
                pkmnNum = boxIDs[j]
                pic = PhotoImage(file='res/{:0>3}.gif'.format(pkmnNum))
                boxPics.append(pic)
            boxDisplay.boxPics = boxPics #avoiding garbage collection
            for pic in boxDisplay.winfo_children():
                pic.destroy()
            for j in range(4):
                for k in range(5):
                    pic = ttk.Label(boxDisplay, image=boxPics[5*j+k])
                    pic.grid(row=j, column=k)
                    
        return buttonFun

    def nextPage():
        global oldBoxNums, newBoxNums

        choices = {i+1:j.current() for i,j in toCombos.items()}
        oldBoxNums = [i for i in choices if choices[i] != 0]
        newBoxNums = [choices[i] for i in oldBoxNums]

        root.nextPage()

    def loadDisplay(*args):
        fromButtons[0].invoke()

    baseFrame = ttk.Frame(root)
    baseFrame.rowconfigure(0, weight=1)
    baseFrame.columnconfigure(0, weight=1)
    baseFrame.bind('<Expose>', loadDisplay)

    
    mainFrame = ttk.Frame(baseFrame, padding=MAIN_PAD)
    mainFrame.grid(row=0, column=0, sticky='nsew')
    mainFrame.rowconfigure(0, weight=1)
    mainFrame.columnconfigure(0, weight=1)
    mainFrame.columnconfigure(1, weight=1)


    boxesFrame = ttk.Frame(mainFrame)
    boxesFrame.grid(row=0, column=0, sticky='w')

    ttk.Label(boxesFrame, text='From').grid(row=0, column=0)
    ttk.Label(boxesFrame, text='To').grid(row=0, column=1)
    
    fromButtons = {}
    toCombos = {}
    #todo: get actual box names
    oldBoxes = ['BOX {}'.format(i+1) for i in range(numBoxes)]
    newBoxes = ['BOX {}'.format(i+1) for i in range(numBoxes)]
    comboChoices = ['None'] + newBoxes
    for i in range(numBoxes):
        fromButtons[i] = ttk.Button(boxesFrame, text='BOX {}'.format(i+1),
                                    command=makeButtonFun(i))
        fromButtons[i].grid(row=i+1, column=0, padx=5)
        toCombos[i] = ttk.Combobox(boxesFrame, values=comboChoices, width=10,
                                   state='readonly')
        toCombos[i].set(comboChoices[0])
        toCombos[i].grid(row=i+1, column=1, padx=5)
    #todo: make sure the same box isn't picked twice

    
    displayFrame = ttk.Frame(mainFrame)
    displayFrame.grid(row=0, column=1)
    DISP_WIDTH = 350

    instrText = 'Use the drop-down menus under the "To" column to choose where the Pok\u00E9mon in the corresponding "From" box will be sent. Boxes marked with "None" will not be transferred. Click the name of the From box to see its contents in the display below.'
    instrLabel = ttk.Label(displayFrame, text=instrText,
                           wraplength=DISP_WIDTH)
    instrLabel.grid(row=0, column=0)

    boxDisplay = ttk.Labelframe(displayFrame)
    boxDisplay.grid(row=1, column=0, pady=20)
    
    #todo: make warning red?
    warning = "WARNING! Any Pok\u00E9mon that previously inhabited chosen boxes in the Gen III save file will be ERASED. It is recommended that you only select empty Gen III boxes."
    warningLabel = ttk.Label(displayFrame, text=warning,
                             wraplength=DISP_WIDTH)
    warningLabel.grid(row=2, column=0)

    navFrame = Nav(baseFrame, root.prevPage, nextPage)
    navFrame.grid(row=1, column=0, sticky='we')

    return (baseFrame, 'Box Selection', {'sticky':'nsew'})

def overwriteWindow(root):
    '''Creates the window for deciding to overwrite or not.'''

    def toggle(*args):    
        setState(choice.get(), 'disabled', [gen2Label, gen3Label,
                                            gen2Button, gen3Button,
                                            gen2Entry, gen3Entry])
        setState(not choice.get(), 'disabled', [warningLabel])

        if not choice.get() and (gen2Text.get() == '' or gen3Text.get() == ''):
            navFrame.disable('next', True)
        else:
            navFrame.disable('next', False)

    def gen2Dialog():
        askSave = filedialog.asksaveasfilename
        file = askSave(title='Gen II Save File', initialdir=root.dir,
                       filetypes=[('GB Save', '.sav'), ('All Files', '.*')],
                       defaultextension='.sav')
        if file != '':
            gen2Text.set(file)
            gen2Entry.after_idle(gen2Entry.xview_moveto, 1)
            root.dir = getDir(file)

    def gen3Dialog():
        askSave = filedialog.asksaveasfilename
        file = askSave(title='Gen III Save File', initialdir=root.dir,
                       filetypes=[('GBA Save', '.sav'), ('All Files', '.*')],
                       defaultextension='.sav')
        if file != '':
            gen3Text.set(file)
            gen3Entry.after_idle(gen3Entry.xview_moveto, 1)
            root.dir = getDir(file)

    def nextPage():
        global newGen2, newGen3, oldGen2, oldGen3

        if choice.get():
            newGen2 = oldGen2
            newGen3 = oldGen3
        else:
            newGen2 = gen2Entry.get()
            newGen3 = gen3Entry.get()

        root.nextPage()

    baseFrame = ttk.Frame(root)
    baseFrame.rowconfigure(0, weight=1)
    baseFrame.columnconfigure(0, weight=1)
    
    
    mainFrame = ttk.Frame(baseFrame, padding=MAIN_PAD)
    mainFrame.grid(row=0, column=0, sticky='ns')
    mainFrame.rowconfigure(0, weight=2)
    mainFrame.rowconfigure(3, weight=1)

    instrText = 'Select whether to overwrite the original save files, or to create new save files.'
    instrLabel = ttk.Label(mainFrame, text=instrText)
    instrLabel.grid(row=0, column=0)


    choiceFrame = ttk.Frame(mainFrame)
    choiceFrame.grid(row=1, column=0)

    choice = BooleanVar(value=True)
    choice1Radio = ttk.Radiobutton(choiceFrame, text='Overwrite',
                                   variable=choice, command=toggle,
                                   value=True)
    choice1Radio.grid(row=0, column=0, pady=5, sticky='w')

    warningText = 'WARNING! Once new data is created, this program can not recover old save data.'
    warningLabel = ttk.Label(choiceFrame, text=warningText, wraplength=300)
    warningLabel.grid(row=1, column=0, pady=5)
    
    choice2Radio = ttk.Radiobutton(choiceFrame, text='Do not overwrite',
                                   variable=choice, command=toggle,
                                   value=False)
    choice2Radio.grid(row=2, column=0, pady=5, sticky='w')


    pickerFrame = ttk.Frame(mainFrame)
    pickerFrame.grid(row=2, column=0)

    gen2Label = ttk.Label(pickerFrame, text='New Gen II file:')
    gen2Label.grid(row=0, column=0, columnspan=2)
    
    gen2Button = ttk.Button(pickerFrame, text='To...', command=gen2Dialog)
    gen2Button.grid(row=1, column=0, sticky='e', padx=5, pady=5)

    gen2Text = StringVar(pickerFrame)
    gen2Text.trace('w', toggle)
    gen2Entry = ttk.Entry(pickerFrame, textvariable=gen2Text, state='readonly')
    gen2Entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    gen3Label = ttk.Label(pickerFrame, text='New Gen III file:')
    gen3Label.grid(row=2, column=0, columnspan=2)
    
    gen3Button = ttk.Button(pickerFrame, text='To...', command=gen3Dialog)
    gen3Button.grid(row=3, column=0, sticky='e', padx=5, pady=5)

    gen3Text = StringVar(pickerFrame)
    gen3Text.trace('w', toggle)
    gen3Entry = ttk.Entry(pickerFrame, textvariable=gen3Text, state='readonly')
    gen3Entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)
    #todo: make sure user doesn't put the same file for both entries


    fillerFrame = ttk.Frame(mainFrame)
    fillerFrame.grid(row=3, column=0, sticky='ns')


    navFrame = Nav(baseFrame, root.prevPage, nextPage)
    navFrame.grid(row=1, column=0, sticky='we')

    if debug:
        gen2Text.set('C:/Users/Sidnoea/Documents/GitHub/pokeBridge/New Gen 2.sav')
        gen3Text.set('C:/Users/Sidnoea/Documents/GitHub/pokeBridge/New Gen 3.sav')
        choice.set(False)

    toggle()

    return (baseFrame, 'Overwrite?', {'sticky':'nsew'})

#todo: flesh this out
def confirmWindow(root):
    '''Displays the confirmation page.'''

    def nextPage():
        '''Brings up the transfer window, initiates the transfer, goes to the
        finalization window when done.'''

        from pokeBridge import transfer
        global oldGen2, newGen2, oldGen3, newGen3
        global oldBoxNums, newBoxNums, newGame, language, gender
        
        root.nextPage()

        transfer(oldGen2, newGen2, oldGen3, newGen3, oldBoxNums, newBoxNums,
                 newGame, language, gender)

        root.nextPage()

    baseFrame = ttk.Frame(root)
    baseFrame.rowconfigure(0, weight=1)
    baseFrame.columnconfigure(0, weight=1)
    

    mainFrame = ttk.Frame(baseFrame)
    mainFrame.grid(row=0, column=0, sticky='nsew')
    mainFrame.rowconfigure(0, weight=1)
    mainFrame.columnconfigure(0, weight=1)

    ttk.Label(mainFrame, text='placeholder text').grid()


    navFrame = Nav(baseFrame, root.prevPage, nextPage)
    navFrame.grid(row=1, column=0, sticky='sew')

    return (baseFrame, 'Confirmation', {'sticky':'nsew'})

def transferWindow(root):
    '''Makes the transfer window.'''

    baseFrame = ttk.Frame(root)
    baseFrame.rowconfigure(0, weight=1)
    baseFrame.columnconfigure(0, weight=1)

    ttk.Label(baseFrame, text='Transferring...').grid()
              
    return (baseFrame, 'Transferring...', {'sticky':'nsew'})

def doneWindow(root):
    '''Makes the succeeded/failed window.'''

    baseFrame = ttk.Frame(root)
    baseFrame.rowconfigure(0, weight=1)
    baseFrame.columnconfigure(0, weight=1)

    ttk.Label(baseFrame, text='Done').grid()

    return (baseFrame, 'Transfer Complete', {'sticky':'nsew'})

def nameHandler(name, message):
    '''Takes a string name and character, provides an interface for correcting
    the illegal name, returns a new legal string name.'''

    #todo: create a proper validate method

    def destroy(*args):
        root.destroy()

    root = Toplevel()
    root.title('Bad Name')
    root.resizable(False, False)
    root.after(100, root.focus_force) #todo: temp?

    mainFrame = ttk.Frame(root, padding=MAIN_PAD)
    mainFrame.grid(column=0, row=0, sticky='nwes')

    newname = StringVar(value=name)

    nameEntry = ttk.Entry(mainFrame, textvariable=newname)
    nameEntry.grid(row=1, sticky='we')

    ttk.Label(mainFrame, text=message).grid(row=0)

    for child in mainFrame.winfo_children():
        child.grid(padx=5, pady=5)

    nameEntry.after(100, nameEntry.focus) #todo: temp?
    root.bind('<Return>', destroy)

    root.wait_window()

    #todo: disable the ability to close the window instead? add abort option?
    if len(newname.get()) < 1:
        return nameHandler(name, message)
    else:
        return newname.get()


if __name__ == '__main__':
    main()
