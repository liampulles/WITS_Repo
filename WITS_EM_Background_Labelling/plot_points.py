from liam_em import LiamEM
import numpy as np
from os import listdir
from os.path import isfile
import cv2
import pickle
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

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

label_files = sorted(listdir("{}/".format("Label")))
#label_files = label_files[:10]
#train_files = listdir("Training/")

print("\nLoading data into memory...")

fdatas = []
bdatas = []

for label_file in label_files:
    full_label = "{}/{}".format("Label",label_file)
    base = label_file[1:-4]
    full_train = "{}/t{}.jpg".format("Training",base)
    print("Processing ({})".format(full_train))
    white,black = extract_data(full_train,full_label,"HSV")
    fdatas += [white]
    bdatas += [black]

fdata = np.vstack(fdatas).astype(np.uint8)
bdata = np.vstack(bdatas).astype(np.uint8)

n = 300

fdata = fdata[np.random.choice(len(fdata),n)]
bdata = bdata[np.random.choice(len(bdata),n)]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c, m, data in [('r', 'o', fdata), ('b', '^', bdata)]:
    xs = data[:,0]
    ys = data[:,1]
    zs = data[:,2]
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')

plt.show()
