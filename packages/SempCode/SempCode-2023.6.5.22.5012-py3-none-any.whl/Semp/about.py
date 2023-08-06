from tkinter import *
from ctypes import OleDLL


OleDLL("shcore").SetProcessDpiAniwareness(1)
class About(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="white")
        self.geometry("1280x768+300+100")
        self.title("About")

def SempAbout():
    if __name__=="__main__":
        About().mainloop()
SempAbout()
