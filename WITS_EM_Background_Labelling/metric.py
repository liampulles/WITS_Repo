from liam_em import LiamEM
import pickle
import numpy as np
import os.path
import sys
import argparse
import cv2

def extract_data(image,mode):
    #print(image,mask)
    img = cv2.imread(image,cv2.IMREAD_COLOR)
    if mode == "HSV":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return img

parser = argparse.ArgumentParser(description='Application to train a LiamEM classifier.')
parser.add_argument('--mask','-m',help='The \"correct\" mask image.',nargs=1,required=True)
parser.add_argument('--test','-t',help='The test image.',nargs=1,required=True)

args = parser.parse_args()

mask = extract_data(args.mask[0],"HSV")
test_in = extract_data(args.test[0],"HSV")
diff = mask - test_in
diff = diff**2
mse = np.average(diff)

print(mse)
