"""
    Semp Write & Reader
    Version:v0.2.6 Beta
"""
from . import Requester


BINARY_TRUE="binary_true_T_WriteBinary"
BINARY_FALSE="binary_false_F_OnlyWrite"


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
        self.returned=self.response.ResponseGet()["text"]
        with open(self.name_filename,"a",encoding=self.encoding) as f:
            f.writelines(self.returned)
    def ResponseAndWriteFile(self,website):
        self.response=Requester(website)
        self.returned=self.response.ResponseGet()["text"]
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

writer=SempWrite