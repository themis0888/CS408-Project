from PIL import Image
import datetime
def matchTemplate(searchImage, templateImage):
    minScore = -1000
    matching_xs = 0
    matching_ys = 0
    searchWidth = searchImage.size[0]
    searchHeight = searchImage.size[1]
    templateWidth = templateImage.size[0]
    templateHeight = templateImage.size[1]
    searchIm = searchImage.load()
    templateIm = templateImage.load()
    #loop over each pixel in the search image
    for xs in range(searchWidth-templateWidth+1):
        for ys in range(searchHeight-templateHeight+1):
        #for ys in range(10):
            #set some kind of score variable to 0
            score = 0
            #loop over each pixel in the template image
            for xt in range(templateWidth):
                for yt in range(templateHeight):
                    score += 1 if searchIm[xs+xt,ys+yt] == templateIm[xt, yt] else -1
            if minScore < score:
                minScore = score
                matching_xs = xs
                matching_ys = ys
                
    print "Location=",(matching_xs, matching_ys), "Score=",minScore
    im1 = Image.new('RGB', (searchWidth, searchHeight), (80, 147, 0))
    im1.paste(templateImage, ((matching_xs), (matching_ys)))
    #searchImage.show()
    #im1.show()
    im1.save('template_matched_in_search.png')
searchImage = Image.open("search_gray.jpg")
templateImage = Image.open("template_gray.jpg")
##searchImage = Image.open("search-500.png")
##templateImage = Image.open("template-80.png")
t1=datetime.datetime.now()
matchTemplate(searchImage, templateImage)
delta=datetime.datetime.now()-t1
print "Time=%d.%d"%(delta.seconds,delta.microseconds)
print "end"