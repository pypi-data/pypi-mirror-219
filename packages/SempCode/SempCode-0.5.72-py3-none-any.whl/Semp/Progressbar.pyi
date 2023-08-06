"""
    Semp-Progressbar
    v0.6.9
"""
from sys import set_int_max_str_digits as max


max(0)
class ChunkError(Exception):
    def __init__(self) -> None: ...

class ProgressbarWarning(Warning):
    def __init__(self) -> None:...

def VirtualProgressbar(description:str = ...,time:int = 0.1)-> None:...

def EasyProgressbar()-> None:...

def DownloadProgressbar(description:str = "Downloading...",website: str = ...,name: str = ...,chunk_size=None)-> None:...

class TkinterProgressBar:
    def __init__(self,url:str = ...,desc:str = ...,title:str = ...,name:str = ...,chunk_size:int = 512,bytes: bool = False,is_parent: bool = True,parent:type = None,notice:str = "")-> None:
        self.w = None
        self.f = None
        self.plan = None
        self.description = None
        self.content = None
        self.chunk_size = None
        self.length = None
        self.name = None
        self.url = None
        self.r = None
        self.notice = None
        self.progressbar = None
        self.progress = None
        self.label = None
        self.word = None
        self.root = None
        ...

    def update_progress(self, value)-> None:...

    def close(self)-> None:...

    def wmclose(self)-> None:...

    def Download(self,mode:str = ...)-> None:...
