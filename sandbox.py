import cv2
import sys
import os
import SAD

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from config import CONFIG

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

im = Image.open('toimage/10.png')
print(im.getdata())