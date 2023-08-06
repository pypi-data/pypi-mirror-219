from requests import *


BINARY_TRUE="binary_true_T_WriteBinary"
BINARY_FALSE="binary_false_F_OnlyWrite"

class Requester:
    def __init__(self, website: str = ...):
        super().__init__()
        self.websitelink = website

    def download(self, name: str = ..., binary=False):
        self.r = get(self.websitelink)
        if binary == True or binary == BINARY_TRUE:
            with open(name, "wb") as f:
                for chunk in self.r.iter_content(chunk_size=512):
                    f.write(chunk)
        # This method can download JPG file, EXE file, PNG file, etc
        elif binary == False or binary == BINARY_FALSE:
            with open(name, "wb") as f:
                for chunk in self.r.iter_content(chunk_size=512):
                    f.write(chunk)
        # This method can download TXT file, JSON file, JS file, etc
        else:
            raise ValueError("Not " + str(name) + ".Expected BINARY_TRUE or BINARY_FALSE")

    def responseget(self):
        self.r = get(self.websitelink)
        return {"status_code": self.r.status_code, "url": self.r.url, "text": self.r.text}

class SempWrite:
    def __init__(self,filename,encoding="utf-8"):
        super().__init__()
        self.name_filename=filename
        self.encoding=encoding
    def ReadAndDeleteAllWord(self,binary=BINARY_FALSE):
        if binary == BINARY_FALSE or binary == False:
            with open(self.name_filename,"r") as f:
                self.variable=f.read()
            with open(self.name_filename,"w",encoding=self.encoding) as f:
                f.write("")
            return self.variable
        elif binary == BINARY_TRUE or binary == True:
            with open(self.name_filename,"rb") as f:
                self.variable=f.read()
            with open(self.name_filename,"wb",encoding=self.encoding) as f:
                f.write("")
            return self.variable
        else:
            raise ValueError("Not be " + str(binary) + ".Expected BINARY_TRUE or BINARY_FALSE")
    def ResponseAndAddFile(self,website):
        self.response=Requester(website)
        self.returned=self.response.responseget()["text"]
        with open(self.name_filename,"a",encoding=self.encoding) as f:
            f.writelines(self.returned)
    def ResponseAndWriteFile(self,website):
        self.response=Requester(website)
        self.returned=self.response.responseget()["text"]
        with open(self.name_filename,"w",encoding=self.encoding) as f:
            f.write(self.returned)
    def OnlyRead(self):
        with open(self.name_filename,"r") as f:
            return f.read()
    def OnlyWrite(self,text):
        with open(self.name_filename,"w",encoding=self.encoding) as f:
            f.write(text)
    def OnlyAdd(self,text):
        with open(self.name_filename,"a",encoding=self.encoding) as f:
            f.write(text)
    def CopyAnotherFileToThisFile(self,filename):
        with open(filename,"r") as f:
            self.copy=f.read()
        with open(self.name_filename,"w",encoding=self.encoding) as f:
            f.write(self.copy)
    def config(self,filename=None,encoding=None):
        if filename != None:
            self.name_filename=filename
        if encoding != None:
            self.encoding=encoding