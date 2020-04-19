from pathlib import Path
import shutil

def rmDir(dirName):
    dirpath = Path(dirName)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)


