"""
    Semp-Progressbar
    v0.6.9
"""
from tqdm import trange,tqdm
from time import sleep
from requests import get
from sys import set_int_max_str_digits as max
from random import randint
from pathlib import Path
from tkinter import *
from tkinter.ttk import Progressbar
from warnings import warn
from ctypes import OleDLL


max(0)
class ChunkError(Exception):
    def __init__(self,*args,**kwargs):
        pass

class ProgressbarWarning(Warning):
    def __init__(self,*args,**kwargs):
        pass

def VirtualProgressbar(description:str = ...,time:int = 0.1):
    bar=tqdm(range(100))
    bar.set_description(description)
    for x in bar:
        sleep(time)

def EasyProgressbar():
    for __count in trange(100):
        sleep(0.1)

def DownloadProgressbar(description:str = "Downloading...",website: str = ...,name: str = ...,chunk_size=None):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
    res = get(website, stream=True, headers=headers)
    length = float(res.headers['content-length'])
    f = open(name, 'wb')
    pbar = tqdm(total=length, initial=Path(name).stat().st_size, unit_scale=True, desc=description, ncols=120)
    if chunk_size == None:
        size=randint(256,5120)
        for chuck in res.iter_content(chunk_size=size):

            pbar.update(len(chuck))
            kb=size/1024
            pbar.set_postfix_str(f"{str(kb)}KB/s")
            f.write(chuck)
        f.close()
    else:
        try:
            temp=chunk_size+114514
        except:
            raise ChunkError("Not a integer value")
        else:
            for chuck in res.iter_content(chunk_size=chunk_size):
                f.write(chuck)
                pbar.update(len(chuck))
                kb = chunk_size / 1024
                pbar.set_postfix_str(f"{str(kb)}KB/s")
            f.close()


class TkinterProgressBar:
    def __init__(self,url:str = ...,desc:str = ...,title:str = ...,name:str = ...,chunk_size:int = 512,bytes: bool = False,is_parent: bool = True,parent:type = None,notice:str = ""):
        warn("This is Alpha Project in SempCode",ProgressbarWarning, stacklevel=2)
        self.url,self.name,self.chunk_size,self.description=url,name,chunk_size,desc
        if is_parent == True:
            self.root=Tk()
        else:
            self.root = Toplevel(parent)
        self.root.wm_geometry("600x400")
        self.root.wm_title(title)
        self.word = StringVar()
        self.label=Label(self.root,textvariable=self.word,font=("Segoe UI",16))
        self.label.pack()
        self.progress = DoubleVar()
        self.progressbar = Progressbar(self.root, variable=self.progress)
        self.progressbar.pack(fill=X)
        self.notice = Label(self.root,text=notice,fg="gray66")
        self.notice.pack(side=BOTTOM)
        self.root.wm_resizable(0,0)
        self.root.wm_protocol("WM_DELETE_WINDOW",lambda :self.wmclose())
        OleDLL("shcore").SetProcessDpiAwareness(1)
        if bytes == True:
            self.Download("wb")
        else:
            self.Download("w")
    def update_progress(self, value):
        self.progress.set(value)
        self.root.update()

    def close(self):
        self.root.destroy()

    def wmclose(self):
        warn("Cannot close window,please wait to download successfully.",ProgressbarWarning, stacklevel=2)
    def Download(self,mode:str = ...):
        self.r=get(self.url,stream=True)
        self.length=int(self.r.headers["content-length"])
        self.content=0
        self.f=open(self.name,mode)
        self.progressbar.configure(maximum=self.length)
        for chunk in self.r.iter_content(chunk_size=self.chunk_size):
            self.content += self.chunk_size
            self.update_progress(self.content)
            self.plan=round((self.content/self.length)*100,1)
            self.word.set(f"{self.description}:{self.plan}% [{self.chunk_size/1024}KB/s]")
            self.f.write(chunk)
        self.close()