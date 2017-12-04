import sys
import os

import time
import client
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from config import CONFIG
from os import walk
cwd = os.getcwd()
sys.path.insert(0, cwd + "/detector")
import findboxes

def detector(selctedImageList):
    return findboxes.detect(selctedImageList)

def classifier():
    client.communicate()
    return read_result()

def read_result():
    tmp = []
    with open('test_result.txt') as f:
        lines = f.readlines()
        tmp = lines
    tmp = [x.strip('\n') for x in tmp]

    result = []
    for i in range(len(tmp)):
        if i%2==1:
            idx = tmp[i].index('_')
            result.append(tmp[i][idx+1:])
        else:
            result.append(tmp[i])
    return result

def parser_detector(result_list):
    coord_list, item_list, value_list = [], [], []
    for i in result_list:
        coord_list.append((i[0],i[1]))
        item_list.append(i[2])
        value_list.append(i[3])
    return coord_list, item_list, value_list

def drawBox(c_result,d_result):
    dic = {}
    categories = []
    for i in range(len(c_result)):
        if (i % 2 == 0):
            # Parse ex) "000.jpg"
            name = c_result[i][:3] + c_result[i][-4:]
            print (name)
            if name in dic:
                dic[name] = dic.get(name) + 1
            else:
                dic[name] = 1
        # get category
        else:
            categories.append(c_result[i])

    # Boxing Result
    images = dic.keys()
    base_index = 0

    print ("Dic, cate")
    print (dic)
    print (categories)

    for img in images:
        outerindex =  base_index + dic.get(img)
        #print ("Drawing %s %d %d" % (img, base_index, outerindex))
        
        findboxes.draw_bounding_box("detector/images/" + img, d_result[base_index : outerindex], categories[base_index : outerindex])
        base_index = base_index + dic.get(img)


# Prepare images
IMGS = []
imgs = os.listdir('detector/images')
for img in imgs:
    IMGS.append('detector/images/' + img)
selctedImageList = IMGS
print (selctedImageList)
print ("Selecting Images Ended")

# Detect
detect_result = detector(selctedImageList)
print ("Detecting Ended")
print (detect_result)

print ("Classifying ...")

# Classifier
#classification_result = classifier()
#print (classification_result)
print (detect_result)

classification_result = read_result()
print(classification_result)

drawBox(classification_result,detect_result)
