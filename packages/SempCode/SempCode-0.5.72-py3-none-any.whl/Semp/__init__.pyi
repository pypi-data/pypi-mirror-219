"""
    Semp Python Tool by Win12Home
    Version:2023.06.05.22.5009 Beta

"""
from sys import set_int_max_str_digits as max


max(0)
BINARY_TRUE = "BTRUE"
BINARY_FALSE = "BFALSE"

AUTO = "AutoEnter"
NONE = "NoEnter"
class NumberError:
    def __init__(self,*args,**kwargs) -> None:...

class BoolError(Exception):
    def __init__(self, *args, **kwargs) -> None:...

class ArgumentError(Exception):
    def __init__(self, *args, **kwargs) -> None:...

class OtherError(Exception):
    def __init__(self, *args, **kwargs) -> None:...

def tkphoto(file:str = ...) -> None:...

def fromsnumber(b_from: int = 0, to: int = ..., passnum: int = 0) -> None:...

def createpassword(length: int = ...) -> None:...

class request_simplifies:
    def download(website: str = ..., name: str = ..., binary=...) -> None:...

    def responseget(website: str = ...) -> None:...

def power_operation(num1: int = ..., num2: int = ...) -> None:...

def fibonacci_sequence(to: int = ...) -> None:...

class requester:
    def __init__(self, website: str = ...) -> None:
        self.r = None
        self.websitelink = None
        ...

    def download(self, name: str = ..., binary=False) -> None:...

    def responseget(self) -> None:...

def pythonprompt() -> None:...

def commandprompt() -> None:...

def createmarkdown(title: str = ..., text: list[str] = ..., name: str = ..., auto: str = AUTO) -> None:...

def gettime(format: str = "%Y.%m.%d %I:%M:%S %p") -> None:...

def nowdate() -> None:...

def date(year: int = ..., month: int = ..., day: int = ...) -> None:...

def dateweekday(datevar) -> None:...

def translator(text:str = ...) -> None:...

class web_search:
    def BingSearch(self,search) -> None:...

    def GoogleSearch(self,search) -> None:...


"""
Here are some examples.
Response(variable):
    response=Requester("https://1.1.1.1/")
    response.ResponseGet()
Response(code):
    request_simplifies.ResponseGet("https://1.1.1.1/")
Fibonacci Sequence:
    fibonacci_sequence(10)
Power:
    power_operation(10,5)
All Numbers:
    fromsnumber(5,135)
Photo TK:
    from tkinter import *
    root=Tk()
    root.title("Test")
    img=PhotoTk("C:/test.jpg")
    a=Label(self,image=img)
    a.pack()
    root.mainloop()
Markdown Creator:
    CreateMarkdown("Hello World!",["They are some example","They are some example"],"README.md")
Translator:
    Translator("Hello World!")
"""