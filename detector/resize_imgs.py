import os
from PIL import Image
def fun():
	path = 'detector/patches'
	files = os.listdir(path)

	for file in files:
	   filename = path + '/' + file
	   img = Image.open(filename)
	   img = img.resize((121,121))
	   img.save(filename)
