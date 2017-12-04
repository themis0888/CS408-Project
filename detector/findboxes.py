#import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches
import selectivesearch
import numpy as np
from PIL import Image, ImageFont, ImageDraw

import resize_imgs
#import sys

def overlap(a, b, margin = 0):
    """ Returns True if two boxes a and b overlaps. Otherwise return False.
        margin is to allow some gap between two boxes.
    """
    a_min_x, a_min_y, a_max_x, a_max_y = a[0],a[1],a[0]+a[2],a[1]+a[3]
    b_min_x, b_min_y, b_max_x, b_max_y = b[0],b[1],b[0]+b[2],b[1]+b[3]
    t = margin
    if ((a_min_x <= b_min_x) and (b_max_x <= a_max_x) and (a_min_y <= b_min_y) and (b_max_y <= a_max_y)):
        # If a includes b, return True regardless of margin
        return True
    elif ((b_min_x <= a_min_x) and (a_max_x <= b_max_x) and (b_min_y <= a_min_y) and (a_max_y <= b_max_y)):
        # If b includes a, return True regardless of margin
        return True
    else: # Doesn't include, but overlap
        if ((a_min_x-t <= b_min_x <= a_max_x+t) and (a_min_y-t <= b_min_y <= a_max_y+t)):
            return True
        elif ((a_min_x-t <= b_max_x <= a_max_x+t) and (a_min_y-t <= b_max_y <= a_max_y+t)):
            return True
        elif ((a_min_x-t <= b_min_x <= a_max_x+t) and (a_min_y-t <= b_max_y <= a_max_y+t)):
            return True
        elif ((a_min_x-t <= b_max_x <= a_max_x+t) and (a_min_y-t <= b_min_y <= a_max_y+t)):
            return True
        else:
            return False

def intersect(group, region, margin):
    """ Return True if the group and region intersects.
        In group, there are many boxes. If region overlaps with any single box,
        this function returns True.
        margin is to allow some gap between boxes.
    """
    for box in group:
        if overlap(box, region, margin=margin) == True:
            return True
    return False

def merge(regions, margin):
    """
    Merge the nearby regions together, producing less number of regions.
    We do this because 'search' returns too many regions.
    ---Algorithm---
    add the first element to group1
    for the second element, if it intersects with group1 more than 30%, add to group1
    else, make a new group called group2, and add it to there.
    for the third element, if it intersects with group1 or group2 more then 30%, add to that group
    else, make a new group called group3, and add it to there.
    ---------------
    """
    groups = []
    for region in regions:
        if len(groups) == 0:
            group = []
            group.append(region)
            groups.append(group)
        else:
            found = False
            for group in groups:
                if intersect(group, region, margin=margin) == True:
                    group.append(region)
                    found = True
                    break
            if found == False:
                group = []
                group.append(region)
                groups.append(group)
    return groups

def find_max(group):
    """ find_max returns single box in group that has maximum area.
    """
    areas = []
    for i in range(len(group)):
        area = (group[i][2]-group[i][0])*(group[i][3]-group[i][1])
        areas.append(area)
    max_area = max(areas)
    index = areas.index(max_area)
    return group[index]

def draw_bounding_box(target_path,boxes,categories):
    """ This gets an image and boxes, and draw boxes on that image.
        After that, save the image as 'result.jpg'
    """
    # NEED TO INSERT CATEGORY
    category_index = 0 

    target = Image.open(target_path)
    target_mat = target.load()

    #print ("draw_bounding_box %s %s" % (target_path), boxes, categories)

    #font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf',16)
    for box in boxes:
        xmin,ymin,xmax,ymax = box[0],box[1],box[0]+box[2],box[1]+box[3]
        width, height = box[2],box[3]
        for i in range(width):
            target_mat[xmin+i,ymin] = (69, 239, 80)
            target_mat[xmin+i,ymax] = (69, 239, 80)
        for j in range(height):
            target_mat[xmin,ymin+j] = (69, 239, 80)
            target_mat[xmax,ymin+j] = (69, 239, 80)

        # Write Text
        draw = ImageDraw.Draw(target)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        # draw.text((x, y),"Sample Text",(r,g,b))
        #print(category)
        category = categories[category_index]
        #draw.text((xmin+2, ymin+height+2),category,(69, 239, 80), font = font)
        draw.text((xmin+2, ymin+height+2),category,(69, 239, 80))
        category_index = category_index + 1

    print(target_path)
    idx = target_path.index('images') + 6
    output = 'result' + target_path[idx:]
    target.save(output)

def search(imagename):
    """ By using selectivesearch package, it searches prominant regions in image,
        and returns candidate boxes. However it returns quite many boxes, so the
        result will be processed by 'merge' later.
    """
    # loading astronaut image
    img = Image.open(imagename)
    img_arr = np.array(img)
    W,H = img.size

    # perform selective search
    img_lbl, regions = selectivesearch.selective_search(
        img_arr, scale=500, sigma=0.8, min_size=200)

    candidates = set()
    for r in regions:
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        if r['size'] < 2000:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        #if w / h > 1.2 or h / w > 1.2:
        #    continue
        if r['rect'][2] >= W - 70 and r['rect'][3] >= H - 70:
            continue
        candidates.add(r['rect'])
        """
    # draw rectangles on the original image
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(img)
    for x, y, w, h in candidates:
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)
    #plt.show()
    """
    return candidates

def crop_bounding_boxes(image,boxes):
    """image: image path to crop"""
    img = Image.open(image)
    cnt = 0
    for box in boxes:
        box = (box[0],box[1],box[0]+box[2],box[1]+box[3])
        patch = img.crop(box)
        idx = image.index('images') + 6
        name = 'detector/patches' + image[idx:-4] + '_' + str(cnt) + '.jpg'
        patch.save(name)
        cnt += 1

def detect(selectedImageList):
    """ main code.
        argv[0] -> find_boxes.py
        argv[1] -> 'image.jpg'
        Then ultimately, 'image_result.jpg' with bounding boxes will be created.
    """
    #img = sys.argv[1]
    result = []
    for img in selectedImageList:
        max_group = []

        regions = search(img)
        # Try many margins, and find the most frequent num_of_group, and use that margin
        margins = [-10,-8,-6,-4,-2,0,2,4,6,8,10]
        num_of_groups = []
        for m in margins:
            max_group = []
            groups = merge(regions,margin=m)
            for group in groups:
                max_group.append(find_max(group))
            num_of_groups.append(len(max_group))
        print(num_of_groups)
        num_of_group = max(set(num_of_groups), key=num_of_groups.count)
        print(num_of_group)
        index = num_of_groups.index(num_of_group)

        max_group = []
        groups = merge(regions,margin=margins[index])
        for group in groups:
            max_group.append(find_max(group))
        print (max_group)
        #draw_bounding_box(img,max_group)
        crop_bounding_boxes(img,max_group)

        # Flatter
        for k in max_group:
            result.append(k)
    #resize
    resize_imgs.fun()
    return result

if __name__ == "__main__":
    detect()
