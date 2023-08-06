"""
    EasyTkinter 2023
    v0.5.5
"""
from tkinter import *
from tkinter.ttk import *
from ttkthemes import *
from ctypes import OleDLL
from subprocess import PIPE,STDOUT
from subprocess import Popen


OleDLL("shcore").SetProcessDpiAwareness(1)

DEFAULT_FONT="Segoe UI"
DEFAULT_THEME="adapta"

class Tk(ThemedTk):
    def __init__(self,theme: str = DEFAULT_THEME):
        super().__init__(theme=theme)
        self.configure(bg="white")

class TextWindow(ThemedTk):
    def __init__(self,label: str = ...,text: str = ...,title: str = "Text",theme: str = DEFAULT_THEME,font: str = DEFAULT_FONT):
        super().__init__(theme=theme)
        self.wm_title(title)
        self.configure(bg="white")
        self.Label=Label(self,text=label,font=(font,10))
        self.Label.pack()
        self.text=Text(self,bd=0,font=(font,8))
        self.text.pack()
        self.text.insert(END, text)
        self.text.configure(state=DISABLED)

        self.exit=Button(self,text="Exit",command=lambda:self.quit())
        self.exit.pack()
        self.mainloop()

class CommandWindow(ThemedTk):
    def __init__(self,theme:str = DEFAULT_THEME,font:str = DEFAULT_FONT):
        super().__init__(theme=theme)
        self.configure(bg="white")
        self.wm_title("Command Prompt")
        self.wm_state("zoomed")

        self.exit=Button(self,text="Exit",command=lambda:self.destroy())
        self.exit.pack(side=BOTTOM)
        self.inputcmd = Button(self, text="Command",command=lambda:self.Input())
        self.inputcmd.pack(side=BOTTOM)
        self.text=Text(self,font=(font,15))
        self.text.pack(fill=BOTH)
        self.text.insert(END,"Windows Console\n")
        self.text["state"]=DISABLED
    def Input(self):
        self.ppppppp=Toplevel()
        Label(self.ppppppp,text="Please input code.").pack()
        self.ppppppp.geometry("600x200")
        self.entry=Entry(self.ppppppp)
        self.entry.pack(fill=X)
        self.ppppppp.configure(bg="white")

        self.button=Button(self.ppppppp,text="Done",command=lambda:self.to_use(command=self.entry.get()))
        self.button.pack()
        self.mainloop()
    def to_use(self,command:str = ...):
        self.ppppppp.destroy()
        self.Use(command=command)
    def Use(self,command:str = ...):
        self.runner=Popen(command,shell=True,stdout=PIPE,stderr=STDOUT,encoding="gb2312")
        self.text["state"]=NORMAL
        self.ms=self.runner.communicate()[0]
        self.msin=str(self.ms)[2:len(self.ms)-6]
        self.text.insert(END,f"{self.ms}\n")
        self.text["state"]=DISABLED
