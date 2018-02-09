import cv2
from os import listdir
from os.path import isfile, splitext
import numpy as np
import pickle
import detect

train_files = sorted(listdir("Training/"),key=lambda x: int(splitext(x[1:])[0]))
data = []
classification = []
for train_file in train_files:
    #if int(splitext(train_file[1:])[0]) <= 199:
    #    continue
    print("Training/{}".format(train_file))
    #train_file = "t200.jpg"
    outimg, ansue, circles, argmax, img = detect.image_process("Training/{}".format(train_file))
    outimg = cv2.cvtColor(outimg,cv2.COLOR_RGB2BGR)
    if not type(circles) == type(None):
        for circle in circles[0]:
            x = circle[0]
            y = circle[1]
            r = circle[2]
            img_crop = img[max(y-100,0):min(y+100,960),max(x-100,0):min(x+100,1280),:]
            outimg_crop = outimg[max(y-100,0):min(y+100,960),max(x-100,0):min(x+100,1280),:]
            disp_img = np.hstack((img_crop,outimg_crop))
            #print(disp_img.shape)
            cv2.imshow('Image',disp_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            ans = input("That was [5,2,1,0.5,0.2,0.1,0]: ")
            classify = 0
            if ans == "0.1":
                classify = 1
            elif ans == "0.2":
                classify = 2
            elif ans == "0.5":
                classify = 3
            elif ans == "1":
                classify = 4
            elif ans == "2":
                classify = 5
            elif ans == "5":
                classify = 6
            else:
                classify = 0
            print("class",classify)
            feature = detect.feauture_extract(circle,circles,argmax)
            data += [feature]
            classification += [classify]
    final = {"data":data,"classes":classification,"lastimage":train_file}
    pickle.dump(final , open( "final.p", "wb" ) )
