
import cv2
import sys
import os
import GUI
import tkinter as TK

import time
import client
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from config import CONFIG
from os import walk
#from detector.find_boxes import detect
cwd = os.getcwd()
sys.path.insert(0, cwd + '/detector')
#print (target)
import findboxes
# Change Every frame of video to images and return Number of images
def video_to_frames(video, path_output_dir):
    vidcap = cv2.VideoCapture(video)
    count = 0
    # Number of Converted Frames
    converted = 0
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            # Capture Every 10 frame
            if(count % 10 == 0):
                # Rotate Clockwise 90
                image = cv2.transpose(image, image)
                image = cv2.flip(image, 1)
                cv2.imwrite(os.path.join(path_output_dir, '{0:03d}.jpg'.format(converted)), image)
                converted += 1
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()
    return converted

# app is GUI App Object
def run(app):
    print ("##### EasyCheckout GUI  #####")

    # Get videofile path from argv
    if (len(sys.argv) == 1):
        print ("Please input Video filename")
        app.changeStatus("Please input Video filename")
        return -1
    videofile = sys.argv[1]
    
    # Convert video to images
    print ("Loading Video File : %s ..." % videofile)
    app.changeStatus("Loading ...\nVideo File")

    count = video_to_frames(videofile, 'detector/images')

    if(count == 0):
        print ("Loading Video failed")
        app.changeStatus("Loading Video\nFAILED")
        return -1
    print ("Total %d frames are converted" % count)
    
    # Selecting proper images to detect
    print ("Selecting Proper Images ...")
    app.changeStatus("Selecting\nImages ...")
    selctedImageList = select_image()
    print ("Selecting Images Ended")
    
    # Detecting images
    app.changeStatus("Detecting...")
    print ("Detecting ...")
    app.update()

    detect_result = detector(selctedImageList)
    print ("Detecting Ended")
    app.changeStatus("Detecing Ended")
    app.update()

    app.changeStatus("Classifying ...")
    print ("Classifying ...")
    app.update()

    # Classifier
    classification_result = classifier()
    #classification_result = read_result()
    #print(classification_result)
    print (classification_result)
    print (detect_result)

    animation = drawBox(classification_result,detect_result)

    # Calculating and Printing Item list
    print ("Your Items")
    #app.changeStatus("Total Cost :\n3,000")
    #detect_result = ["socks","rice","cup","snack","tape"]
    #GUI_showItems(app,detect_result)

    f = []
    for (a,b,filenames) in walk('result/'):
        f.extend(filenames)

    for name in filenames:

        time.sleep(0.5)
        app.changeImage("result/" + name,resize = False)
       
        items = animation[name]
        print (animation)
        print (name)
        print (items)
        price = calculator(items)
        app.changeStatus("Total Cost :\n%d" % (price[1]))
        GUI_showItems(app, items)
        app.update()
        app.clearItem()
        

    #time.sleep(10)
    #app.changeImage("toimage/24.png")

    
    #a, b = calculator(detect_result)
    #print (a)
    #print (b)
    
    #app.changeStatus("Total Cost:\n %d" % (b))
    
    print ("############ END #############")
    
    # Comment
    # If we want to reuse the program (ex : end of the program, return start)
    # It is better to get input in the program, not argv
    # and then make another function main() in the initialize function
    




def select_image():
    # select proper image to detect
    # from pre-built images
    # save image to another directory
    IMGS = []
    imgs = os.listdir('detector/images')
    for img in imgs:
        IMGS.append('detector/images/' + img)
    return IMGS

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
#print(result)

'''
def detector(testimage):
    # Basic Detector
    positions_category = []
    classes = ["cup","glasscase","greenbar","pencilcase","rice","scissors","shave","snack","socks","spaghetti","tape"]
    
    for i in range(10):
        template_name = "templates_small/" + classes[i] + ".jpg"
        target_name = testimage
        positions_category.append(SAD.find_in_image(template_name, target_name))
        SAD.draw_bounding_box(target_name, positions_category, 20, 36)
    
    print(positions_category)
    SADs = []
    for e in positions_category:
        SADs.append(e[3])
    SADs.sort()
    print(SADs)
'''

'''
parser_detector : list -> list, list, list
parser_detector : result list from detector -> coordinate list, item list, value list
'''
def parser_detector(result_list):
    coord_list, item_list, value_list = [], [], []
    for i in result_list:
        coord_list.append((i[0],i[1]))
        item_list.append(i[2])
        value_list.append(i[3])
    return coord_list, item_list, value_list


'''
calculator : list of string -> list of int, int
calculator : item list -> list of cost, total cost 
'''
def calculator(item_list = []):
    # print the item list and price
    if len(item_list) == 0:
        print("Err : empty item list")
        return None
    total_cost = 0
    cost_list = []
    for j in item_list:
        cost_list.append(CONFIG[j])
        if CONFIG[j] == 'end':
            break
        total_cost += CONFIG[j]

    return  cost_list, total_cost

# print(calculator(parser_detector(input_list)[1]))

# Show Items on GUI
def GUI_showItems(app, item_list = []):
    for item in item_list:
        app.insertItem(item)

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

    animation = {}

    for img in images:
        outerindex =  base_index + dic.get(img)
        #print ("Drawing %s %d %d" % (img, base_index, outerindex))
        
        findboxes.draw_bounding_box("detector/images/" + img, d_result[base_index : outerindex], categories[base_index : outerindex])
        animation[img] = categories[base_index : outerindex]
        base_index = base_index + dic.get(img)
        

    # For Animation
    return animation


# Program Starts from Here
if __name__ == '__main__':
    guiFrame = TK.Tk()
    guiFrame.geometry("500x420")
    app = GUI.App(guiFrame)
    guiFrame.mainloop()