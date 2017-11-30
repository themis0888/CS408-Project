from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def find_in_image(template,target):
    im1 = Image.open(template)
    im2 = Image.open(target)
    im1_mat = im1.load()
    im2_mat = im2.load()
    width1, height1 = im1.size
    width2, height2 = im2.size

    bestSAD = 1000000000
    bestX = -1
    bestY = -1
    for x in range(0,width2-width1,15):
        for y in range(0,height2-height1,15):
            SAD = 0.0
            for i in range(0,width1,2):
                for j in range(0,height1,3):
                    SAD += abs(abs(im2_mat[x+i,y+j][0] - im1_mat[i,j][0])+
                    abs(im2_mat[x+i,y+j][1] - im1_mat[i,j][1])+
                    abs(im2_mat[x+i,y+j][2] - im1_mat[i,j][2]))
            if bestSAD > SAD:
                bestX = x
                bestY = y
                bestSAD = SAD

    if "cup" in template:
        category = "cup"
    elif "glasscase" in template:
        category = "glasscase"
    elif "greenbar" in template:
        category = "greenbar"
    elif "pencilcase" in template:
        category = "pencilcase"
    elif "rice" in template:
        category = "rice"
    elif "scissors" in template:
        category = "scissors"
    elif "shave" in template:
        category = "shave"
    elif "snack" in template:
        category = "snack"
    elif "socks" in template:
        category = "socks"
    elif "spaghetti" in template:
        category = "spaghetti"
    elif "tape" in template:
        category = "tape"

    return (bestX,bestY, category, bestSAD)

def draw_bounding_box(target_path,positions_category,width,height):
    target = Image.open(target_path)
    target_mat = target.load()
    #font = ImageFont.truetype("sans-serif.ttf", 16)
    for pos_cate in positions_category:
        bestX = pos_cate[0]
        bestY = pos_cate[1]
        category = pos_cate[2]
        for i in range(width):
            target_mat[bestX+i,bestY+height] = (32, 20, 255)
            target_mat[bestX+i,bestY] = (32, 20, 255)
        for j in range(height):
            target_mat[bestX,bestY+j] = (32, 20, 255)
            target_mat[bestX+width,bestY+j] = (32, 20, 255)
        # Write Text
        draw = ImageDraw.Draw(target)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        # draw.text((x, y),"Sample Text",(r,g,b))
        #print(category)
        draw.text((bestX+2, bestY+height+2),category,(255, 0, 0))
    target.save("result.jpg")

if __name__ == "__main__":
    positions_category = []
    classes = ["cup","glasscase","greenbar","pencilcase","rice","scissors","shave","snack","socks","spaghetti","tape"]

    for i in range(10):
        template_name = "templates_small/" + classes[i] + ".jpg"
        #target_name = "test_images/KakaoTalk_Video_20171002_1733_58_402 16.jpg"
        target_name = "test_images/KakaoTalk_Video_20171002_1735_21_045 20.jpg"
        positions_category.append(find_in_image(template_name, target_name))
        draw_bounding_box(target_name, positions_category, 20, 36)

    print(positions_category)
    SADs = []
    for e in positions_category:
        SADs.append(e[3])
    SADs.sort()
    print(SADs)








"""
im1 = Image.open("templates_small/greenbar.jpg")
im2 = Image.open("test_images/KakaoTalk_Video_20171002_1733_58_402 16.jpg")

im1_mat = im1.load()
im2_mat = im2.load()

width1, height1 = im1.size
width2, height2 = im2.size

bestSAD = 1000000000
bestX = -1
bestY = -1
#print((width2-width1)*(height2-height1)/25*width1*height1)
for x in range(0,width2-width1,15):
    for y in range(0,height2-height1,15):
        SAD = 0.0
        for i in range(0,width1,2):
            for j in range(0,height1,3):
                SAD += abs(abs(im2_mat[x+i,y+j][0] - im1_mat[i,j][0])+
                abs(im2_mat[x+i,y+j][1] - im1_mat[i,j][1])+
                abs(im2_mat[x+i,y+j][2] - im1_mat[i,j][2]))
        if bestSAD > SAD:
            bestX = x
            bestY = y
            bestSAD = SAD

im3 = Image.new(im2.mode, im2.size)
im3 = im2.copy()
im3_mat = im3.load()

# Draw a output picture with bounding box
for i in range(width1):
    im3_mat[bestX+i,bestY+height1] = (32, 20, 255)
    im3_mat[bestX+i,bestY] = (32, 20, 255)
for j in range(height1):
    im3_mat[bestX,bestY+j] = (32, 20, 255)
    im3_mat[bestX+width1,bestY+j] = (32, 20, 255)
im3.save("result.jpg")
"""
