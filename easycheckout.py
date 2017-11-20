import cv2
import sys
import os
import SAD

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Change Every frame of video to images and return Number of images
def video_to_frames(video, path_output_dir):
    vidcap = cv2.VideoCapture(video)
    count = 0
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            # Capture Every 10 frame
            if(count % 10 == 0):
                cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, image)
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()
    return count;

def initialize():
    print ("##### EasyCheckout Beta  #####")
    
    # Get videofile path from argv
    if (len(sys.argv) == 1):
        print ("Please input Video filename")
        return -1
    videofile = sys.argv[1]
    
    # Convert video to images
    print ("Loading Video File : %s ..." % videofile)
    count = video_to_frames(videofile, 'toimage')
    if(count == 0):
        print ("Loading Video failed")
        return -1
    print ("Total %d frames are converted" % count)
    
    # Selecting proper images to detect
    print ("Selecting Proper Images ...")
    select_image()
    # TEMP FOR DEMO
    selimg1 = "toimage/190.png"
    print ("Selecting Images Ended")
    
    # Detecting images
    print ("Detecting ...")
    detector(selimg1)
    print ("Detecting Ended")
    
    # Calculating and Printing Item list
    print ("Your Items")
    calculator()
    
    print ("############ END #############")
    
    # Comment
    # If we want to reuse the program (ex : end of the program, return start)
    # It is better to get input in the program, not argv
    # and then make another function main() in the initialize function


def select_image():
    # select proper image to detect
    # from pre-built images
    # save image to another directory
    pass

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

def calculator():
    # print the item list and price
    pass


# Program Starts from Here    
initialize()
