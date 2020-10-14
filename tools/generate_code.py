import base64
from photo import *
from PIL import Image
from io import BytesIO

# Convert a list of file to string format

with open("del.png", "rb") as imageFile:
    code_delete = base64.b64encode(imageFile.read())

with open("new.png", "rb") as imageFile:
    code_new = base64.b64encode(imageFile.read())

with open("save.png", "rb") as imageFile:
    code_save = base64.b64encode(imageFile.read())

with open("bigger.png", "rb") as imageFile:
    code_bigger = base64.b64encode(imageFile.read())


with open("smaller.png", "rb") as imageFile:
    code_smaller = base64.b64encode(imageFile.read())

with open("close.png", "rb") as imageFile:
    code_close = base64.b64encode(imageFile.read())

with open("photo.py", "w") as save:
    save.write("code_delete="+str(code_delete)+"\ncode_new="+str(code_new)+"\ncode_save="+str(code_save)+"\ncode_bigger="+str(code_bigger)+"\ncode_smaller="+str(code_smaller)+"\ncode_close="+str(code_close))

