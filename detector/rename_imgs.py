import os
path = '/mnt/hdd/akalsdnr/2017Fall/4_CS_Project/find_boxes/images'
files = os.listdir(path)
i = 0

for file in files:
  os.rename(os.path.join(path,file), os.path.join(path, str(i)+'.jpg'))
  i += 1
