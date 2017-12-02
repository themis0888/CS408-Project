import cv2
import sys
import os
import SAD
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from config import CONFIG
from scipy.misc import imshow
import numpy as np
from config import CONFIG
from os import walk

from scipy import signal
from scipy import misc



#name_list = ['cup', 'glasscase', 'pencilcase', 'rice', 'scissors', 'shave', 'snack', 'socks', 'spaghetti', 'tape']
name_list = ['greenbar']
def video_to_frames(video, path_output_dir, cnt = 0):
    vidcap = cv2.VideoCapture(video)
    count = cnt
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            # Capture Every 10 frame
            if(count % 1 == 0):
                cv2.imwrite(os.path.join(path_output_dir, '{0:03d}.jpg'.format(count)), image)
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()
    return count

"""
for i in range(len(name_list)):
    f = []
    filenames = []
    for (dirpath, dirnames, filenames) in walk(str(i+1) + '_' + name_list[i]+'/'):
        print(str(i+1) + '_' + name_list[i]+'/')
        f.extend(filenames)
    c = 0
    for name in filenames:
        c = video_to_frames(str(i+1) + '_' + name_list[i]+'/'+name, str(i+1) + '_' + name_list[i], cnt = c)


"""
for i in range(len(name_list)):
    f = []
    filenames = []
    for (dirpath, dirnames, filenames) in walk(str(i+1) + '_' + name_list[i]+'/'):
        print(str(i+1) + '_' + name_list[i]+'/')
        f.extend(filenames)
    c = 0
    for name in filenames:
        if 'mp4' in name:
            continue
        im2 = Image.open(str(i+1) + '_' + name_list[i]+'/'+name)

        # select the template imabe from current image. 
        im1 = im2.crop((int(im2.size[0]/2-im2.size[1]/2),0,int(im2.size[0]/2+im2.size[1]/2),im2.size[1]))

        # shrink the image for operation speed, and this still not affect to the performance
        # Here!!!! you can resize this part!!!!! 
        ratio = 0.3
        im = im1.resize( [int(ratio * s) for s in im1.size] )
        im.save(str(i+1) + '_' + name_list[i]+'/'+name)


"""
f = []
for (dirpath, dirnames, filenames) in walk('COCA/'):
    f.extend(filenames)

for name in filenames:
    im

im2 = Image.open("toimage/110.png")

# select the template imabe from current image. 
im1 = im2.crop((0,0.15*im2.size[1],0.3*im2.size[0],0.85*im2.size[1]))
ratio = 0.3

#searchImage1 = Image.open("test_bg.jpg")
#im1 = Image.open("cup.jpg")


# shrink the image for operation speed, and this still not affect to the performance
searchImage = searchImage1.resize( [int(ratio * s) for s in searchImage1.size] )

"""