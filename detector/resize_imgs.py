import os
from PIL import Image
path = '/mnt/hdd/akalsdnr/2017Fall/4_CS_Project/find_boxes/patches'
files = os.listdir(path)

for file in files:
   filename = path + '/' + file
   img = Image.open(filename)
   img = img.resize((121,121))
   img.save(filename)
