from tkinter import *
from tkinter import ttk

def nameHandler(name, message):
    '''Takes a string name and character, provides an interface for correcting
    the illegal name, returns a new legal string name.'''

    def end(*args):
        if len(newname.get()) > 0:
            root.destroy()

    root = Tk()
    root.title("Bad Name")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    newname = StringVar()
    newname.set(name)

    name_entry = ttk.Entry(mainframe, textvariable=newname)
    name_entry.grid(row=2, sticky=(W, E))

    ttk.Label(mainframe, text=message).grid(row=1, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    name_entry.focus()
    root.bind('<Return>', end)

    root.mainloop()

    #todo: disable the ability to close the window instead? add abort option?
    if len(newname.get()) < 1:
        return nameHandler(name, message)
    else:
        return newname.get()
