import base64

def convertfile(count,classIdentity):
    outfile = "{}Class={}.jpg".format(count,classIdentity)
    base64file = "{}Class={}.xml".format(count,classIdentity)
    with open(outfile, "rb") as imageFile:
        string = base64.b64encode(imageFile.read())
    with open(base64file,"wb") as f:
        f.write(string)
        f.close()
