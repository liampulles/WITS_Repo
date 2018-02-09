import cv2
from os import listdir
from os.path import isfile
import numpy as np
import sklearn.covariance
import pickle

def multi_norm_pdf(x,mean,covar):
    return

def extract_data(image,mask):
    img = cv2.imread(image,cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    msk = cv2.imread(mask,cv2.IMREAD_COLOR)
    msk = cv2.cvtColor(msk, cv2.COLOR_BGR2GRAY)
    indices = np.where(msk >= 128)
    #print(img[indices])
    return img[indices]

def load():
    black_plastic = np.zeros((0,3),dtype=np.uint8)
    blue_pen = np.zeros((0,3),dtype=np.uint8)
    copper = np.zeros((0,3),dtype=np.uint8)
    gold = np.zeros((0,3),dtype=np.uint8)
    ruler = np.zeros((0,3),dtype=np.uint8)
    silver = np.zeros((0,3),dtype=np.uint8)
    purple_plastic = np.zeros((0,3),dtype=np.uint8)
    background = np.zeros((0,3),dtype=np.uint8)

    train_files = sorted(listdir("Training/"))
    black_plastic_files = listdir("Black_Plastic/")
    blue_pen_files = listdir("Blue_Pen/")
    background_files = listdir("Background/")
    copper_files = listdir("Copper/")
    gold_files = listdir("Gold/")
    purple_plastic_files = listdir("Purple_Plastic/")
    ruler_files = listdir("Ruler/")
    silver_files = listdir("Silver/")

    #Data extraction
    print("\n+++++Loading+++++")
    for train_file in train_files:
        full_train = "Training/{}".format(train_file)
        print("Processing",train_file)
        base = train_file[1:-4]

        if "bpl{}.png".format(base) in black_plastic_files:
            out = extract_data(full_train,"Black_Plastic/bpl{}.png".format(base))
            black_plastic = np.vstack((black_plastic,out)).astype(np.uint8)

        if "b{}.png".format(base) in background_files:
            out = extract_data(full_train,"Background/b{}.png".format(base))
            background = np.vstack((background,out)).astype(np.uint8)

        if "bp{}.png".format(base) in blue_pen_files:
            out = extract_data(full_train,"Blue_Pen/bp{}.png".format(base))
            blue_pen = np.vstack((blue_pen,out)).astype(np.uint8)

        if "c{}.png".format(base) in copper_files:
            out = extract_data(full_train,"Copper/c{}.png".format(base))
            copper = np.vstack((copper,out)).astype(np.uint8)

        if "g{}.png".format(base) in gold_files:
            out = extract_data(full_train,"Gold/g{}.png".format(base))
            gold = np.vstack((gold,out)).astype(np.uint8)

        if "p{}.png".format(base) in purple_plastic_files:
            out = extract_data(full_train,"Purple_Plastic/p{}.png".format(base))
            purple_plastic = np.vstack((purple_plastic,out)).astype(np.uint8)

        if "r{}.png".format(base) in ruler_files:
            out = extract_data(full_train,"Ruler/r{}.png".format(base))
            ruler = np.vstack((ruler,out)).astype(np.uint8)

        if "s{}.png".format(base) in silver_files:
            out = extract_data(full_train,"Silver/s{}.png".format(base))
            silver = np.vstack((silver,out)).astype(np.uint8)

    #Mean calc, Covariance estimation
    black_plastic_mean = np.mean(black_plastic,axis=0)
    black_plastic_cov = sklearn.covariance.empirical_covariance(black_plastic, assume_centered=False)
    background_mean = np.mean(background,axis=0)
    background_cov = sklearn.covariance.empirical_covariance(background, assume_centered=False)
    blue_pen_mean = np.mean(blue_pen,axis=0)
    blue_pen_cov = sklearn.covariance.empirical_covariance(blue_pen, assume_centered=False)
    copper_mean = np.mean(copper,axis=0)
    copper_cov = sklearn.covariance.empirical_covariance(copper, assume_centered=False)
    gold_mean = np.mean(gold,axis=0)
    gold_cov = sklearn.covariance.empirical_covariance(gold, assume_centered=False)
    purple_plastic_mean = np.mean(purple_plastic,axis=0)
    purple_plastic_cov = sklearn.covariance.empirical_covariance(purple_plastic, assume_centered=False)
    ruler_mean = np.mean(ruler,axis=0)
    ruler_cov = sklearn.covariance.empirical_covariance(ruler, assume_centered=False)
    silver_mean = np.mean(silver,axis=0)
    silver_cov = sklearn.covariance.empirical_covariance(silver, assume_centered=False)

    print("\n=====Loading Results=====")
    print("Black Plastic:",black_plastic.shape,black_plastic_mean,black_plastic_cov)
    print("Background:",background.shape,background_mean,background_cov)
    print("Blue Pen:",blue_pen.shape,blue_pen_mean,blue_pen_cov)
    print("Copper:",copper.shape,copper_mean,copper_cov)
    print("Gold:",gold.shape,gold_mean,gold_cov)
    print("Purple Plastic:",purple_plastic.shape,purple_plastic_mean,purple_plastic_cov)
    print("Ruler:",ruler.shape,ruler_mean,ruler_cov)
    print("Silver:",silver.shape,silver_mean,silver_cov)

    print("\n+++++Saving Results...+++++")
    final = [{'title':"Black Plastic",'mean':black_plastic_mean,'cov':black_plastic_cov}]
    final += [{'title':"Background",'mean':background_mean,'cov':background_cov}]
    final += [{'title':"Blue Pen",'mean':blue_pen_mean,'cov':blue_pen_cov}]
    final += [{'title':"Copper",'mean':copper_mean,'cov':copper_cov}]
    final += [{'title':"Gold",'mean':gold_mean,'cov':gold_cov}]
    final += [{'title':"Purple Plastic",'mean':purple_plastic_mean,'cov':purple_plastic_cov}]
    final += [{'title':"Ruler",'mean':ruler_mean,'cov':ruler_cov}]
    final += [{'title':"Silver",'mean':silver_mean,'cov':silver_cov}]

    pickle.dump( final, open( "data.p", "wb" ) )

load()
