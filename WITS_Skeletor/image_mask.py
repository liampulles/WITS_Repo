import numpy as np
from os import listdir
from os.path import isfile
import cv2
import pickle
import sys
from sklearn.decomposition import PCA
#from scipy.stats import multivariate_normal
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.svm import SVC
#from sklearn.gaussian_process import GaussianProcessClassifier
#from sklearn.ensemble import AdaBoostClassifier

colors = [[0,0,0]] #Black
colors += [[0,0,255]] #Blue
colors += [[0,255,0]] #Green
colors += [[255,0,0]] #Red
colors += [[255,255,255]] #White
colors += [[255, 204, 0]] #Yellow
colors += [[102, 51, 0]] #DarkPiece
colors += [[217, 179, 140]] #WhitePiece

norms = pickle.load( open( "norms.p", "rb" ) )

def argmax_label(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #weights = [1,1,1,1,1,1,1,1]

    orig_shape = rgb.shape

    #color_imgs = np.zeros((orig_shape[0],orig_shape[1],orig_shape[2],0),np.uint8)
    #for i in range(len(colors)):
    #    color_img = np.zeros((orig_shape[0],orig_shape[1],orig_shape[2]),np.uint8)
    #    color_img[:] = colors[i]
        #print(color_img.reshape((orig_shape[0],orig_shape[1],orig_shape[2],1)).shape)
    #    color_imgs = np.concatenate((color_imgs,color_img.reshape((orig_shape[0],orig_shape[1],orig_shape[2],1))),axis=3)
    #print(color_imgs[:,:,:,0].shape)

    #probs = np.zeros((orig_shape[0],orig_shape[1],0))
    x = rgb.reshape(-1,3)
    x = norms['pca'].transform(x)

    #for i,label in [(0,'black'),(1,'blue'),(2,'green'),(3,'red'),(4,'white'),(5,'yellow'),(6,'darkpiece'),(7,'whitepiece')]:
    #    prob = multivariate_normal.pdf(x,mean=norms[label]['mean'],cov=norms[label]['cov']).reshape(orig_shape[0],orig_shape[1],1)*norms[label]['weight']
        #print(prob.shape)
        #print(probs.shape)
    #    probs = np.concatenate((probs,prob),axis=2)
    #argmaxs = np.argmax(probs,axis=2)
    #print(x.shape)

    #argmaxs = norms['knn'].predict(x)
    #argmaxs = norms['dtc'].predict(x)
    argmaxs = norms['gnb'].predict(x)
    #argmaxs = norms['qda'].predict(x)
    #argmaxs = norms['abc'].predict(x)
    argmaxs = argmaxs.reshape((orig_shape[0],orig_shape[1]))
    #print(argmaxs.shape)

    outimg = np.zeros(orig_shape,dtype=np.uint8)
    for i in range(len(colors)):
        mask = (argmaxs == i)
        outimg[mask] = colors[i]
    #print(np.max(argmaxs))
    #outimg = probs[argmaxs,colors]
    #print(np.select(condlist,colors))
    #print(outimg.dtype)
    return cv2.cvtColor(outimg, cv2.COLOR_RGB2BGR), argmaxs

for image in range(1,10):
    img = cv2.imread('Training/{}.png'.format(image),cv2.IMREAD_COLOR)
    #img = cv2.medianBlur(img,5)
    outimg, argmaxs = argmax_label(img)
    cv2.imshow('Image',outimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
