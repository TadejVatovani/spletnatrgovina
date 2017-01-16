from PIL import Image
import os
size=300,300


for filename in os.listdir('./izdelki/'):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"): 
        size=300,300
        im = Image.open('./izdelki/'+filename)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save('./izdelki/'+filename,'JPEG')
    else:
       continue

