from tkinter import *
from tkinter.simpledialog import Dialog

class LabeledEntry(Frame):
    def __init__(self, parent, *args, **kargs):
        text = kargs.pop("text")
        Frame.__init__(self, parent)
        self.label = Label(self, text=text, justify=LEFT).grid(sticky = W, column=0,row=0)
        self.entry = Entry(self, *args, **kargs).grid(sticky = E, column=1, row=0)

class User_Input(Dialog):
    def body(self, parent):
        fields = ['Text Label 1', 'This is the text Label 2']
        # GUIFrame =Frame(parent)
        # GUIFrame.pack(expand=True, anchor=NW)
        # parent.minsize(width=350, height=325)
        field_index = 1
        for field in fields:
            self.field = LabeledEntry(self, text=field)
            self.field.grid(column=0, row=field_index)
            self.field.grid_columnconfigure(index = 0, minsize = 150)
            field_index += 1
        # self.Button2 = Button(parent, text='exit', command= parent.quit)
        # self.Button2.place(x=25, y=300)

    def apply(self):
        print('hello')
        print(self.field.entry.get())

root = Tk()

MainFrame =User_Input(root)
print(MainFrame.field)
root.mainloop()
