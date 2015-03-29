#todo: when do I need root.mainloop()?

#Window process: main() makes one window, each function adds its own elements
#to the window on entry and wipes the window contents on exit/before calling
#the next function. Each window has its own nav button functions.

debug = True

from tkinter import *
from tkinter import ttk

WIDTH = 600
HEIGHT = 450
MAIN_PAD = 10

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
        self.dir = getcwd() #todo: this probably belongs elsewhere

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.mainFrame = ttk.Frame()
##        self.load(0)

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

    def mainloop(self):
        '''Starts the main loop.'''

        self.load(0)
        super().mainloop()

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

    return fileName[:fileName.rfind('\\')]

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
    '''Sets up the initial window.'''

    root = Root([title, filePicker, boxPicker, overwritePicker])
    root.geometry('{}x{}'.format(WIDTH, HEIGHT))
    root.resizable(False, False)

    root.mainloop()

def title(root):
    '''Creates the title window.'''

    baseFrame = ttk.Frame(root)
    baseFrame.rowconfigure(0, weight=1)
    baseFrame.columnconfigure(0, weight=1)

    
    mainFrame = ttk.Frame(baseFrame, padding=MAIN_PAD)
    mainFrame.grid(row=0, column=0, sticky='n')

    titleLabel = ttk.Label(mainFrame, text='PokeBridge')
    titleLabel.grid(row=0, column=1)

    bodyText = '''Hello, and welcome to PokeBridge! This simple application will allow you to transfer your Pok\u00E9mon from Generation II to Generation III, moving entire Boxes at a time. To get started, press the Next button.'''
    bodyLabel = ttk.Label(mainFrame, text=bodyText, justify='center',
                          wraplength=500)
    bodyLabel.grid(row=1, column=0, columnspan=3)

    pic1 = PhotoImage(file='res\\old025.png')
    pic1Label = ttk.Label(mainFrame, image=pic1)
    pic1Label.grid(row=0, column=0)

    pic2 = PhotoImage(file='res\\025.png')
    pic2Label = ttk.Label(mainFrame, image=pic2)
    pic2Label.grid(row=0, column=2)
    
    mainFrame.pics = [pic1, pic2] #need this to avoid garbage collection...


    navFrame = Nav(baseFrame, root.prevPage, root.nextPage)
    navFrame.grid(row=1, column=0, sticky='we')
    navFrame.hide('back', True)

    return (baseFrame, 'PokeBridge', {'sticky':'nsew'})

def filePicker(root):
    '''Makes the window that lets the user specify save files and options.'''

    def nextToggle(*args, **kwargs):
        if fromText.get() == '' or toText.get() == '':
            navFrame.disable('next', True)
        else:
            navFrame.disable('next', False)

    def fromDialog():
        file = filedialog.askopenfilename(title='Gen II Save File',
                                          filetypes=[('GB Save', '.sav'),
                                                     ('All Files', '.*')],
                                          initialdir=root.dir)
        if file != '':
            fromText.set(file)
            fromEntry.after(100, fromEntry.xview_moveto, 1) #todo: why??
            root.dir = getDir(file)
    
    def toDialog():
        file = filedialog.askopenfilename(title='Gen III Save File',
                                          filetypes=[('GBA Save', '.sav'),
                                                     ('All Files', '.*')],
                                          initialdir=root.dir)
        if file != '':
            toText.set(file)
            toEntry.after(100, toEntry.xview_moveto, 1) #todo: why??
            root.dir = getDir(file)

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
    pickLabel = ttk.Label(pickerFrame, text=pickText)
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


    navFrame = Nav(baseFrame, root.prevPage, root.nextPage)
    navFrame.grid(row=1, column=0, sticky='we')

    if debug:
        fromText.set('debug.sav')
        toText.set('debug.sav')

    nextToggle()

    #todo: don't allow user to leave this page until valid files are specified
    #todo: save vars on exit

    return (baseFrame, 'Select Save Files', {'sticky':'nsew'})

def boxPicker(root):
    '''Creates the window for selecting the boxes to be transferred.'''
    from pokeBridge import SaveGame

    def makeButtonFun(i):
        def buttonFun():
            boxDisplay['text'] = comboChoices[i+1]
        return buttonFun
    
    numBoxes = SaveGame.NUMBER_OF_BOXES

    baseFrame = ttk.Frame(root)
    baseFrame.rowconfigure(0, weight=1)
    baseFrame.columnconfigure(0, weight=1)

    
    mainFrame = ttk.Frame(baseFrame, padding=MAIN_PAD)
    mainFrame.grid(row=0, column=0, sticky='nwe')
    mainFrame.columnconfigure(0, weight=1)
    mainFrame.columnconfigure(1, weight=1)


    boxesFrame = ttk.Frame(mainFrame)
    boxesFrame.grid(row=0, column=0, sticky='w')

    ttk.Label(boxesFrame, text='From').grid(row=0, column=0)
    ttk.Label(boxesFrame, text='To').grid(row=0, column=1)
    
    fromButtons = {}
    toCombos = {}
    comboTexts = {i:StringVar(value='None') for i in range(numBoxes)}
    boxesFrame.comboTexts = comboTexts #avoiding garbage collection
    #todo: get actual box names
    comboChoices = ['None'] + ['BOX {}'.format(i+1) for i in range(numBoxes)]
    for i in range(numBoxes):
        fromButtons[i] = ttk.Button(boxesFrame, text='BOX {}'.format(i+1),
                                    command=makeButtonFun(i))
        fromButtons[i].grid(row=i+1, column=0, padx=5)
        toCombos[i] = ttk.Combobox(boxesFrame, values=comboChoices, width=10,
                                   textvariable=comboTexts[i],
                                   state='readonly')
        toCombos[i].grid(row=i+1, column=1, padx=5)
    #todo: make buttons load pictures

    
    displayFrame = ttk.Frame(mainFrame)
    displayFrame.grid(row=0, column=1, sticky='we')
    DISP_WIDTH = 350

    instrText = 'Use the drop-down menus under the "To" column to choose where the Pok\u00E9mon in the corresponding "From" box will be sent. Boxes marked with "None" will not be transferred. Click the name of the From box to see its contents in the display below.'
    instrLabel = ttk.Label(displayFrame, text=instrText,
                           wraplength=DISP_WIDTH)
    instrLabel.grid(row=0, column=0)

    boxDisplay = ttk.Labelframe(displayFrame, text=comboChoices[1])
    boxDisplay.grid(row=1, column=0, pady=20)
    
    pic = PhotoImage(file="res\\000.png")
    displayFrame.pic = pic #avoiding garbage collection
    for i in range(5):
        for j in range(4):
            ttk.Label(boxDisplay, image=pic).grid(column=i, row=j)
    
    #todo: make warning red?
    warning = "WARNING! Any Pok\u00E9mon that previously inhabited chosen boxes in the Gen III save file will be ERASED. It is recommended that you only select empty Gen III boxes."
    warningLabel = ttk.Label(displayFrame, text=warning,
                             wraplength=DISP_WIDTH)
    warningLabel.grid(row=2, column=0)


    navFrame = Nav(baseFrame, root.prevPage, root.nextPage)
    navFrame.grid(row=1, column=0, sticky='we')

    return (baseFrame, 'Box Selection', {'sticky':'nsew'})

def overwritePicker(root):
    '''Creates the window for deciding to overwrite or not.'''
    
    def toggle():
        setState(choice.get(), 'disabled', [gen2Label, gen3Label,
                                            gen2Button, gen3Button,
                                            gen2Entry, gen3Entry])
        setState(not choice.get(), 'disabled', [warningLabel])

    def gen2Dialog():
        file = filedialog.asksaveasfilename(title='Gen II Save File',
                                            filetypes=[('GB Save', '.sav'),
                                                       ('All Files', '.*')],
                                            defaultextension='.sav',
                                            initialdir=root.dir)
        if file != '':
            gen2Text.set(file)
            gen2Entry.after(100, gen2Entry.xview_moveto, 1)
            root.dir = getDir(file)

    def gen3Dialog():
        file = filedialog.asksaveasfilename(title='Gen III Save File',
                                            filetypes=[('GBA Save', '.sav'),
                                                       ('All Files', '.*')],
                                            defaultextension='.sav',
                                            initialdir=root.dir)
        if file != '':
            gen3Text.set(file)
            gen3Entry.after(100, gen3Entry.xview_moveto, 1)
            root.dir = getDir(file)

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
    gen2Entry = ttk.Entry(pickerFrame, textvariable=gen2Text, state='readonly')
    gen2Entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    gen3Label = ttk.Label(pickerFrame, text='New Gen III file:')
    gen3Label.grid(row=2, column=0, columnspan=2)
    
    gen3Button = ttk.Button(pickerFrame, text='To...', command=gen3Dialog)
    gen3Button.grid(row=3, column=0, sticky='e', padx=5, pady=5)

    gen3Text = StringVar(pickerFrame)
    gen3Entry = ttk.Entry(pickerFrame, textvariable=gen3Text, state='readonly')
    gen3Entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)

    toggle()


    fillerFrame = ttk.Frame(mainFrame)
    fillerFrame.grid(row=3, column=0, sticky='ns')


    navFrame = Nav(baseFrame, root.prevPage, root.nextPage)
    navFrame.grid(row=1, column=0, sticky='we')
    navFrame.hide('next', True)
    #todo: if do not overwrite is picked, don't allow user to leave this page
    #      until valid file locations are specified

    return (baseFrame, 'Overwrite?', {'sticky':'nsew'})

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
        child.grid(padx=5, pady=5)

    nameEntry.focus()
    root.bind('<Return>', end)

    #todo: disable the ability to close the window instead? add abort option?
    if len(newname.get()) < 1:
        return nameHandler(name, message)
    else:
        return newname.get()



if __name__ == '__main__':
    main()
