find_boxes.py

0. Environment
python 2.7, 3.6
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
import numpy as np
from PIL import Image
import sys


1. How to run
<Directory>
/find_boxes.py
/myimg.jpg

<Command>
$ python find_boxes.py myimg.jpg

<Output>
myimg_result.jpg


2. Functions
def overlap(a, b, margin = 0):

def intersect(group, region, margin):

def merge(regions, margin):

def find_max(group):

def draw_bounding_box(target_path,boxes):

def search(imagename):

def main():
