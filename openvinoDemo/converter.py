import base64
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d, %H:%M")
def convertfile(count, classIdentity):
    outfile = "{}{}{}.jpg".format(count, classIdentity, now)
    base64file = "{}{}{}.xml".format(count, classIdentity, now)
    with open(outfile, "rb") as imageFile:
        string = base64.b64encode(imageFile.read())
    with open(base64file,"wb") as f:
        f.write(string)
        f.close()
