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
parser.add_argument('--classifier','-e',help='Classifier file. Default \"em.p\".',nargs=1,required=False,default=["em.p"])
parser.add_argument('--input','-i',help='Input images.',nargs='+',required=True)
parser.add_argument('--output','-o',help='Output directory. Default \".\".',nargs=1,required=False,default=["."])
parser.add_argument('--colorspace','-c',help='Colorspace to use. Default \"HSV\" (Otherwise \"BGR\").',nargs=1,required=False,default=["HSV"])
parser.add_argument('--invert','-n',help='Invert the mask. Off by default.',action='store_true',required=False)
parser.add_argument('--flip','-f',help='Invert the bernoulli parameter. Off by default.',action='store_true',required=False)

args = parser.parse_args()
if len(args.input) == 0:
    sys.exit(0)

if args.colorspace[0] not in ["HSV","BGR"]:
    print("Invalid colorspace")
    sys.exit(0)

em = pickle.load( open( args.classifier[0], "rb" ) )

for image in args.input:
    print("Processing {}".format(image))
    img = extract_data(image,args.colorspace[0])
    orig_shape = img.shape
    mask = em.classify(np.array(img,dtype=np.uint8).reshape(orig_shape[0]*orig_shape[1],orig_shape[2]),args.invert,args.flip).reshape((orig_shape[0],orig_shape[1]))
    outname = os.path.split(image)[1][:-4]
    cv2.imwrite("{}/{}_mask.png".format(args.output[0],outname), mask)
