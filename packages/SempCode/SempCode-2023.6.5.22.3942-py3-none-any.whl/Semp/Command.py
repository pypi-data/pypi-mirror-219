"""
    SempCommand Alpha
    Version:a109
"""
from subprocess import run
from pathlib import Path
from datetime import datetime
from os import system


EXIST_TRUE=True
EXIST_FALSE=False
class ModeError(Exception):
    def __init__(self, *args, **kwargs):
        pass
class Commander:
    def __init__(self):
        super().__init__()
    def RunCommand(self,command: str = ...,shell: bool = True):
        run(command,shell=shell)
    def path_exist(self,path: str = ...):
        if Path(path).exists():
            return EXIST_TRUE
        else:
            return EXIST_FALSE
    def create_path(self,path:str = ...,parents:bool = False):
        Path(path).mkdir(parents=parents)
    def path_is_dir(self,path: str = ...):
        return Path(path).is_dir()
    def path_is_file(self,path: str = ...):
        return Path(path).is_file()
    def remove_file(self,path: str = ...):
        Path(path).unlink(missing_ok=True)
    def remove_directory(self,path: str = ...):
        Path(path).rmdir()
    def file_size(self,path: str = ...):
        return Path(path).stat().st_size
    def file_time(self,path: str = ...,mode: int = 1):
        if mode == 0:
            self.time=Path(path).stat().st_mtime
            self.date=datetime.utcfromtimestamp(self.time)
            return self.date.strftime("%Y.%m.%d %H:%M:%S")
        elif mode == 1:
            self.time = Path(path).stat().st_ctime
            self.date = datetime.utcfromtimestamp(self.time)
            return self.date.strftime("%Y.%m.%d %H:%M:%S")
        else:
            raise ModeError("Because not in 0&1")
    def rename(self,path: str = ...,new_name: str = ...):
        Path(path).rename(new_name)
    def systemcommand(self,command: str = ...):
        system(command)