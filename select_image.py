import datetime
#import cv2
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

from scipy import signal
from scipy import misc


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def matchTemplate3(searchImage, templateImage):
    minScore = -1000
    matching_xs = 0
    matching_ys = 0
    searchWidth = searchImage.size[0]
    searchHeight = searchImage.size[1]
    templateWidth = templateImage.size[0]
    templateHeight = templateImage.size[1]
    searchIm = searchImage.load()
    templateIm = templateImage.load()
    #loop over each pixel in the search image
    for xs in range(0,searchWidth-templateWidth+1,5):
        for ys in range(0,searchHeight-templateHeight+1,5):
        #for ys in range(10):
            #set some kind of score variable to 0
            '''
            score = 0
            #loop over each pixel in the template image
            for xt in range(templateWidth):
                for yt in range(templateHeight):
                    score += 1 if searchIm[xs+xt,ys+yt] == templateIm[xt, yt] else -1
            if minScore < score:
                minScore = score
                matching_xs = xs
                matching_ys = ys
            '''
            score = 0
            #loop over each pixel in the template image
            for xt in range(templateWidth):
                for yt in range(templateHeight):
                    score  += abs(abs(searchIm[xs+xt,ys+yt][0] - templateIm[xt, yt][0])+
                    abs(searchIm[xs+xt,ys+yt][1] - templateIm[xt, yt][1])+
                    abs(searchIm[xs+xt,ys+yt][2] - templateIm[xt, yt][2]))
            if minScore < score:
                minScore = score
                matching_xs = xs
                matching_ys = ys

                
    print( "Location={} \t Score= {}".format(matching_xs, matching_ys, minScore))
    im1 = Image.new('RGB', (matching_xs, matching_ys), (80, 147, 0))
    im1.paste(searchImage, (0,0))
    #searchImage.show()
    #im1.show()
    im1.save('template_matched_in_search.png')
    return im1

'''
matchTemplate : Image Image -> tuple of integer
get the source image and template image, and return the coordination 
of the template image. 
'''
def matchTemplate(searchImage, templateImage):
    searchWidth = searchImage.size[0]
    searchHeight = searchImage.size[1]
    templateWidth = templateImage.size[0]
    templateHeight = templateImage.size[1]
    si = np.asarray(searchImage)
    ti = np.asarray(templateImage)
    si = si - si.mean()
    ti = ti - si.mean()
    ti = ti - ti.mean()
    # give it a noise (because source image doesn't contain the exact same image)
    si = si + np.random.randn(*si.shape) * 5
    corr = signal.correlate2d(si,ti,boundary = 'symm', mode = 'same')
    y,x = np.unravel_index(np.argmax(corr), corr.shape)

    # make the checking image 
    '''
    im1 = Image.new('RGB', (searchWidth, searchHeight), (80, 147, 0))
    im1.paste(searchImage, (0,0))
    im1.paste(templateImage, (x-int(templateWidth/2),y-int(templateHeight/2)))
    print('Location : {},{}'.format(x,y))
    #searchImage.show()
    #im1.show()
    im1.save('template_matched_in_search.png')
    '''
    return (x,y)


# search image is the latter one. 
searchImage1 = Image.open("toimage/120.png")
templateImage2 = Image.open("toimage/110.png")

# select the template imabe from current image. 
templateImage1 = templateImage2.crop((0,0.15*templateImage2.size[1],0.3*templateImage2.size[0],0.85*templateImage2.size[1]))
ratio = 0.3

#searchImage1 = Image.open("test_bg.jpg")
#templateImage1 = Image.open("cup.jpg")


# make this as a grayscale image. 
searchImage1 = searchImage1.convert('L')
templateImage1 = templateImage1.convert('L')

# shrink the image for operation speed, and this still not affect to the performance
searchImage = searchImage1.resize( [int(ratio * s) for s in searchImage1.size] )
templateImage = templateImage1.resize( [int(ratio * s) for s in templateImage1.size] )

t1=datetime.datetime.now()
im = matchTemplate(searchImage, templateImage)
im.show()

delta=datetime.datetime.now()-t1
print("Time=%d.%d"%(delta.seconds,delta.microseconds))
print("end")
