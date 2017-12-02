#import cv2
#import sys
#import os
import SAD
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


# Ex) draw_bounding_box(im, [[20,30,'cup',400]], 40,50)
def draw_bounding_box(target,positions_category,t_width,t_height):
    target_mat = target.load()
    for pos_cate in positions_category:
        bestX = int(pos_cate[0])
        bestY = int(pos_cate[1])
        width = min(t_width, target.size[0]-bestX-1)
        height = min(t_height, target.size[1]-bestY-1)
        category = pos_cate[2]
        for i in range(width):
            target_mat[bestX+i,bestY+height] = (32, 20, 255)
            target_mat[bestX+i,bestY] = (32, 20, 255)
        for j in range(height):
            target_mat[bestX,bestY+j] = (32, 20, 255)
            target_mat[bestX+width,bestY+j] = (32, 20, 255)
        # Write Text
        draw = ImageDraw.Draw(target)

        draw.text((bestX+2, bestY+height+2),category,(255, 0, 0))
    target.save("result2.jpg")
    return target


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
    max_corr = np.argmax(corr)
    y,x = np.unravel_index(max_corr, corr.shape)

    im1 = Image.new('RGB', (searchWidth, searchHeight), (80, 147, 0))
    im1.paste(searchImage, (0,0))
    im1.paste(templateImage, (x-int(templateWidth/2),y-int(templateHeight/2)))
    print('Location : {},{}'.format(x,y))
    im1.save('template_matched_in_search.png')

    return (x, y, max_corr)


# search image is the latter one. 
searchImage = Image.open("toimage/170.png")
#templateImage = Image.open("toimage/160.png")

ratio = 0.3

#searchImage = Image.open("test_bg.jpg")
rawImage = searchImage
templateImage = Image.open("pattern/cup.png")

# make this as a grayscale image. 
searchImage = searchImage.convert('L')
templateImage = templateImage.convert('L')

# shrink the image for operation speed, and this still not affect to the performance
searchImage = searchImage.resize( [int(ratio * s) for s in searchImage.size] )
templateImage = templateImage.resize( [int(ratio * s) for s in templateImage.size] )
rawImage = rawImage.resize( [int(ratio * s) for s in rawImage.size] )
# select the template image from current image. 
#templateImage = templateImage.crop((0,0.15*templateImage.size[1],0.3*templateImage.size[0],0.85*templateImage.size[1]))

x, y, corr = matchTemplate(searchImage, templateImage)

searchedImage = searchImage.crop((x - int(templateImage.size[0]/2), y - int(templateImage.size[1]/2),
    x + int(templateImage.size[0]/2), y + int(templateImage.size[1]/2)))
searchedImage = searchedImage.resize( [s for s in templateImage.size] )

a = np.asarray(searchedImage.getdata())
b = np.asarray(templateImage.getdata())
diff = np.sum(abs(a-b))

#if diff < 100000:
    #return [x, y, 'cup', diff]

draw_bounding_box(rawImage, [[x - int(templateImage.size[0]/2),y - int(templateImage.size[1]/2),'cup',diff]], 
    templateImage.size[0], templateImage.size[1]).show()
print('diff is : {}'.format(diff))







