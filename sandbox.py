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

source = Image.open("test_bg.jpg")
temp = Image.open("cup.jpg")
source = source.convert('L')
temp  = temp.convert('L')
#face = np.array(source.getdata(),np.uint8) #.reshape(source.size)
    #+np.array(source.getdata())[:,1].reshape(source.size)
    #+np.array(source.getdata())[:,2].reshape(source.size))
face = np.asarray(source)
template = np.asarray(temp)
face = face - face.mean()
#template = np.copy(face[300:365, 670:750])  # right eye
template = template - face.mean()
template = template - template.mean()
face = face + np.random.randn(*face.shape) * 5  # add noise
corr = signal.correlate2d(face, template, boundary='symm', mode='same')
y, x = np.unravel_index(np.argmax(corr), corr.shape)  # find the match

import matplotlib.pyplot as plt
fig, (ax_orig, ax_template, ax_corr) = plt.subplots(3, 1,
                                                    figsize=(6, 15))
ax_orig.imshow(face, cmap='gray')
ax_orig.set_title('Original')
ax_orig.set_axis_off()
ax_template.imshow(template, cmap='gray')
ax_template.set_title('Template')
ax_template.set_axis_off()
ax_corr.imshow(corr, cmap='gray')
ax_corr.set_title('Cross-correlation')
ax_corr.set_axis_off()
ax_orig.plot(x, y, 'ro')
fig.show()