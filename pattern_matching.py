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
from os import walk

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


# Ex) draw_bounding_box(im, [[20,30,'cup',400]])
def draw_bounding_box(target,positions_category, filename):
    target_mat = target.load()
    for pos_cate in positions_category:
        bestX = max(int(pos_cate[0]), 0)
        bestY = max(int(pos_cate[1]), 0)
        width = min(int(pos_cate[4]), target.size[0]-bestX-2)
        height = min(int(pos_cate[5]), target.size[1]-bestY-2)
        category = pos_cate[2]
        
        for i in range(width):
            target_mat[bestX+i,bestY+height] = (32, 20, 255)
            target_mat[bestX+i,bestY] = (32, 20, 255)
        for j in range(height):
            target_mat[bestX,bestY+j] = (32, 20, 255)
            target_mat[bestX+width,bestY+j] = (32, 20, 255)
        # Write Text
        draw = ImageDraw.Draw(target)

        draw.text((bestX+2, bestY+2),category,(255, 0, 0))
    target.save("result/" + filename)
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
    '''
    im1 = Image.new('RGB', (searchWidth, searchHeight), (80, 147, 0))
    im1.paste(searchImage, (0,0))
    im1.paste(templateImage, (x-int(templateWidth/2),y-int(templateHeight/2)))
    im1.save('template_matched_in_search.png')
    '''
    return (x, y, max_corr)

def resizeImage(searchIm, tempIm):
    # search image is the latter one. 
    searchImage = Image.open(searchIm)
    #templateImage = Image.open("toimage/160.png")

    ratio = 0.3

    #searchImage = Image.open("test_bg.jpg")
    rawImage = searchImage
    templateImage = Image.open(tempIm)

    # make this as a grayscale image. 
    searchImage = searchImage.convert('L')
    templateImage = templateImage.convert('L')

    # shrink the image for operation speed, and this still not affect to the performance
    searchImage = searchImage.resize( [int(ratio * s) for s in searchImage.size] )
    templateImage = templateImage.resize( [int(ratio * s) for s in templateImage.size] )
    #rawImage = rawImage.resize( [int(ratio * s) for s in rawImage.size] )
    # select the template image from current image. 
    #templateImage = templateImage.crop((0,0.15*templateImage.size[1],0.3*templateImage.size[0],0.85*templateImage.size[1]))
    return searchImage, templateImage, rawImage, ratio


item_list = ['cup', 'glasscase', 'pencilcase', 'rice', 'shaver', 'socks', 'spaghetti', 'tape']

def find_item(item_list):
    f = []
    for (a,b,filenames) in walk('toimage/'):
        f.extend(filenames)

    for name in filenames:
        print('File : {}'.format(name))
        result_list = []
        for item in CONFIG:
            searchImage, templateImage, rawImage, ratio = resizeImage('toimage/' + name, 'pattern/'+ item + '.png')
            t_width, t_height = templateImage.size
            x, y, corr = matchTemplate(searchImage, templateImage)

            searchedImage = searchImage.crop((x - int(templateImage.size[0]/2), y - int(templateImage.size[1]/2),
                x + int(templateImage.size[0]/2), y + int(templateImage.size[1]/2)))
            searchedImage = searchedImage.resize( [s for s in templateImage.size] )

            a = np.asarray(searchedImage.getdata())
            b = np.asarray(templateImage.getdata())
            diff = np.sum(abs(a-b))

            if diff < 50000:
                print('Location : {},{} \tItem : {}\tDiff : {}'.format(x,y, item, diff))
                result_list.append([(x - int(t_width/2))/ratio, 
                    (y - int(t_height/2))/ratio, item, diff, t_width/ratio, t_height/ratio])
        draw_bounding_box(rawImage, result_list, name)
        



find_item(item_list)
#draw_bounding_box(rawImage, result_list).show()








