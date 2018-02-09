from liam_em import LiamEM
import numpy as np
from os import listdir
from os.path import isfile
import cv2
import pickle
import argparse
import sys

def extract_data(image,mask,mode):
    #print(image,mask)
    img = cv2.imread(image,cv2.IMREAD_COLOR)
    if mode == "HSV":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    msk = cv2.imread(mask,cv2.IMREAD_COLOR)
    msk = cv2.cvtColor(msk, cv2.COLOR_BGR2GRAY)
    white_indices = np.where(msk >= 128)
    black_indices = np.where(msk < 128)
    #print(img[indices])
    return img[white_indices], img[black_indices]

parser = argparse.ArgumentParser(description='Application to train a LiamEM classifier.')
parser.add_argument('--labels','-l',help='Labels image path. Default \"Label\".',nargs=1,required=False,default=["Label"])
parser.add_argument('--training','-t',help='Training image path. Default \"Training\".',nargs=1,required=False,default=["Training"])
parser.add_argument('--bdists','-b',help='Number of background distributions. Default 2.',nargs=1,required=False,default=[2])
parser.add_argument('--fdists','-f',help='Number of foreground distributions. Default 2.',nargs=1,required=False,default=[2])
parser.add_argument('--percent','-p',help='Percentage of input data to be used as samples. Default 0.1.',nargs=1,required=False,default=[0.1])
parser.add_argument('--output','-o',help='Pickle file to save to. Default \"em.p\".',nargs=1,required=False,default=["em.p"])
parser.add_argument('--colorspace','-c',help='Colorspace to use. Default \"HSV\" (Otherwise \"BGR\").',nargs=1,required=False,default=["HSV"])
parser.add_argument('--iterations','-i',help='Max number of EM step iterations. Default 100.',nargs=1,required=False,default=[100])
args = parser.parse_args()

if args.colorspace[0] not in ["HSV","BGR"]:
    print("Invalid colorspace")
    sys.exit(0)

label_files = sorted(listdir("{}/".format(args.labels[0])))
#label_files = label_files[:10]
#train_files = listdir("Training/")

print("\nLoading data into memory...")

fdatas = []
bdatas = []

for label_file in label_files:
    full_label = "{}/{}".format(args.labels[0],label_file)
    base = label_file[1:-4]
    full_train = "{}/t{}.jpg".format(args.training[0],base)
    print("Processing ({})".format(full_train))
    white,black = extract_data(full_train,full_label,args.colorspace)
    fdatas += [white]
    bdatas += [black]

fdata = np.vstack(fdatas).astype(np.uint8)
bdata = np.vstack(bdatas).astype(np.uint8)

percent = float(args.percent[0])

fdata = fdata[np.random.choice(len(fdata),int(fdata.shape[0]*percent))]
bdata = bdata[np.random.choice(len(bdata),int(bdata.shape[0]*percent))]

print(bdata.shape)
#fdata = fdata[:int(fdata.shape[0]*percent),:]
#bdata = bdata[:int(fdata.shape[0]*percent),:]
#print(fdata.shape)
#input("stop")
#fdata = np.random.shuffle(fdata)#[:int(fdata.shape[0]*0.1),:]
#bdata = np.random.shuffle(bdata)
#print(fdata)
#fdata = fdata[:int(fdata.shape[0]*0.1),:]
#bdata = bdata[:int(bdata.shape[0]*0.1),:]

print("\nTraining on data...")
em = LiamEM(int(args.bdists[0]),int(args.fdists[0]))
prop = fdata.shape[0]/float(bdata.shape[0]+fdata.shape[0])
em.train(bdata,fdata,int(args.iterations[0]),prop)

print("Dumping trained EM classifier...")
pickle.dump( em, open( args.output[0], "wb" ) )
