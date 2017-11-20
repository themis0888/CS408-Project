from PIL import Image
import sys

filename = sys.argv[1]

img = Image.open(filename)
img = img.resize((20,36))
img.save(filename)
