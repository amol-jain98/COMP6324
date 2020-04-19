import base64
from datetime import datetime

def convertfile(filename):
    with open(filename, "rb") as imageFile:
        string = base64.b64encode(imageFile.read())
    return string
