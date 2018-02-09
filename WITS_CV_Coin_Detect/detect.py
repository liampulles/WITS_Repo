import cv2
import argparse
import pickle
import numpy as np
from scipy.stats import multivariate_normal
from sklearn.ensemble import RandomForestClassifier

norms = pickle.load( open( "data.p", "rb" ) )
clf = pickle.load( open( "forest.p", "rb" ) )

def feauture_extract(circle,circles,argmax):
    x = circle[0]
    y = circle[1]
    r = circle[2]
    count_s, total = count_under_circle(x,y,r,argmax,[7])
    count_c, total = count_under_circle(x,y,r,argmax,[3])
    count_g, total = count_under_circle(x,y,r,argmax,[4])
    count_cg, total = count_under_circle(x,y,r,argmax,[3,4])
    count_crap, total = count_under_circle(x,y,r,argmax,[2,5,6])
    outring_s, total = count_under_ring(x,y,r,r+20,argmax,[7])
    outring_c, total = count_under_ring(x,y,r,r+20,argmax,[3])
    outring_g, total = count_under_ring(x,y,r,r+20,argmax,[4])
    outring_cg, total = count_under_ring(x,y,r,r+20,argmax,[3,4])
    outring_crap, total = count_under_ring(x,y,r,r+20,argmax,[2,5,6])
    inring_s, total = count_under_ring(x,y,r-20,r,argmax,[7])
    inring_c, total = count_under_ring(x,y,r-20,r,argmax,[3])
    inring_g, total = count_under_ring(x,y,r-20,r,argmax,[4])
    inring_cg, total = count_under_ring(x,y,r-20,r,argmax,[3,4])
    inring_crap, total = count_under_ring(x,y,r-20,r,argmax,[2,5,6])
    overlap_now = circle_intersection(circle,circles)
    overlap_grow = circle_intersection((x,y,r+20),circles)
    overlap = (overlap_grow>overlap_now)

    feature = [r]
    feature += [count_s,count_c,count_g,count_cg,count_crap]
    feature += [outring_s,outring_c,outring_g,outring_cg,outring_crap]
    feature += [inring_s,inring_c,inring_g,inring_cg,inring_crap]
    feature += [overlap]
    #print(feature)
    return feature

def clamp(minval,val,maxval):
    return sorted((minval, val, maxval))[1]

def count_under_circle(x,y,r,argmax,mats):
    win = r
    (tot_y,tot_x) = argmax.shape
    top = clamp(0,tot_y-y,win)
    bottom = clamp(0,y,win)
    left = clamp(0,x,win)
    right = clamp(0,tot_x-x,win)
    crop = argmax[y-bottom:y+top,x-left:x+right]
    #print(crop.shape)
    mask = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(win*2,win*2))
    mask = mask[win-bottom:(win*2)+(win-top),win-left:(win*2)+(win-right)]
    select = np.zeros(crop.shape,dtype=np.uint8)
    for mat in mats:
        select += (crop==mat)
    count = np.sum(select[np.where(mask)])
    total = np.sum(mask)
    #cv2.imshow('Image',mask*255)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return count, total

def count_under_ring(x,y,r1,r2,argmax,mats):
    count_2,total_2 = count_under_circle(x,y,r2,argmax,mats)
    count_1,total_1 = count_under_circle(x,y,r1,argmax,mats)
    #print(count_2,count_1,total_2,total_1)
    return count_2-count_1, total_2-total_1

def circle_intersection(circle_check,circles):
    count = 0
    for circle in circles[0]:
        dist = (((circle_check[0]-circle[0])**2)+((circle_check[1]-circle[1])**2))**0.5
        #Same circle?
        if dist < 0.1:
            continue
        if dist < circle_check[2] + circle[2]:
            count += 1
    return count

def argmax_label(hsv):
    colors = [[255,0,0]]
    colors += [[255,191,0]]
    colors += [[127,255,0]]
    colors += [[0,255,63]]
    colors += [[0,255,255]]
    colors += [[0,63,255]]
    colors += [[127,0,255]]
    colors += [[255,0,191]]

    weights = [0.5,2,1,2,2,1,1,0.5]
    #weights = [1,1,1,1,1,1,1,1]

    orig_shape = hsv.shape

    #color_imgs = np.zeros((orig_shape[0],orig_shape[1],orig_shape[2],0),np.uint8)
    #for i in range(len(colors)):
    #    color_img = np.zeros((orig_shape[0],orig_shape[1],orig_shape[2]),np.uint8)
    #    color_img[:] = colors[i]
        #print(color_img.reshape((orig_shape[0],orig_shape[1],orig_shape[2],1)).shape)
    #    color_imgs = np.concatenate((color_imgs,color_img.reshape((orig_shape[0],orig_shape[1],orig_shape[2],1))),axis=3)
    #print(color_imgs[:,:,:,0].shape)

    probs = np.zeros((orig_shape[0],orig_shape[1],0))
    x = hsv.reshape(-1,3)

    for i in range(len(colors)):
        prob = multivariate_normal.pdf(x,mean=norms[i]['mean'],cov=norms[i]['cov']).reshape(orig_shape[0],orig_shape[1],1)*weights[i]
        #print(prob.shape)
        #print(probs.shape)
        probs = np.concatenate((probs,prob),axis=2)
    argmaxs = np.argmax(probs,axis=2)
    outimg = np.zeros(orig_shape,dtype=np.uint8)
    for i in range(len(colors)):
        mask = (argmaxs == i)
        outimg[mask] = colors[i]
    #print(np.max(argmaxs))
    #outimg = probs[argmaxs,colors]
    #print(np.select(condlist,colors))
    #print(outimg.dtype)
    return cv2.cvtColor(outimg, cv2.COLOR_RGB2BGR), argmaxs

def multi_norm_pdf(x,mean,cov):
    #print(((((2*np.pi)**len(mean))*np.linalg.det(cov))**0.5))
    return np.exp(-0.5*np.transpose(x-mean).dot(np.linalg.inv(cov)).dot(x-mean))/((((2*np.pi)**len(mean))*np.linalg.det(cov))**0.5)

def main_detect():
    parser = argparse.ArgumentParser(description='Module and application to detect coins in an image.')
    parser.add_argument('--input','-i',help='Input image path.',nargs=1,required=True)
    parser.add_argument('--silent','-s',help='Don\'t show an image.',action='store_true',required=False)
    parser.add_argument('--demo','-d',help='Explain the steps along the way.',action='store_true',required=False)
    args = parser.parse_args()
    outimg, value, circles, argmax, orig = image_process(args.input[0],args.demo)
    if not args.silent:
        cv2.imshow('Image',outimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("Value is:",value)

def value_map(cla):
    val = 0
    if cla == 1:
        val = 0.1
    elif cla == 2:
        val = 0.2
    elif cla == 3:
        val = 0.5
    elif cla == 4:
        val = 1
    elif cla == 5:
        val = 2
    elif cla == 6:
        val = 5
    else:
        val = 0
    return val

def image_process(filename,demo=False):
    img = cv2.imread(filename,cv2.IMREAD_COLOR)
    if demo:
        print("- (input image)")
        cv2.imshow('Image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("input.jpg", img)
    k = 127
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))

    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #rgb = cv2.cvtColor(morph, cv2.COLOR_HSV2RGB)

    #median = (median - 10)*1.1
    # Convert BGR to HSV
    #median = hsv
    #median = cv2.normalize(median, median, alpha=20, beta=200, norm_type=cv2.NORM_MINMAX)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #lap = cv2.Laplacian(cv2.GaussianBlur(hsv,(5,5),0)[:,:,2],cv2.CV_8U)*10
    #
    #red_diff = (img[:,:,1]+k)/(img[:,:,0]+k)
    #frame = cv2.bilateralFilter(frame,9,75,75)
    frame  = cv2.addWeighted(hsv[:,:,1], 0.5, hsv[:,:,2], 0.5,0)
    if demo:
        print("- Converted the image to the HSV color space")
        print("- Combined the saturation and value channels together.")
        cv2.imshow('Image',frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("sat-val.jpg", frame)
    min_pix = 30
    max_pix = 180
    frame = (((frame-min_pix).astype(np.float64)/float(max_pix-min_pix))*255).astype(np.uint8)
    if demo:
        print("- Performed a fixed contrast stretch on the image")
        cv2.imshow('Image',frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("cont.jpg", frame)
    #print(np.min(frame),np.max(frame))
    pts1 = np.float32([[180,0],[1090,0],[40,960],[1240,960]])
    pts2 = np.float32([[130,0],[1140,0],[130,960],[1140,960]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(frame,M,(1280,960))
    dst = cv2.copyMakeBorder(dst,50,50,50,50,cv2.BORDER_CONSTANT,value=(0,0,0))
    if demo:
        print("- Did a perspective transform on the image, and added borders")
        cv2.imshow('Image',dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("pers.jpg", dst)
    #dst[dst==0] = 128
    frame = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel,iterations=1)
    #frame = cv2.bilateralFilter(frame,9,75,75)
    frame = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel,iterations=1)
    if demo:
        print("- Did a closing, then an opening on the image using a circular element of radius 10")
        cv2.imshow('Image',frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("morph.jpg", frame)
    #frame = ((hsv[:,:,1].astype(np.float64)+hsv[:,:,2].astype(np.float64))/2.0).astype(np.uint8)
#    frame = (((frame-min_pix).astype(np.float64)/float(max_pix-min_pix))*255).astype(np.uint8)
    #frame = cv2.bilateralFilter(frame,9,75,75)
    #frame = cv2.addWeighted(frame, 1.5, gauss, -0.5,0)
    #frame = cv2.bilateralFilter(((frame-30).astype(np.float64)*1.3).astype(np.uint8),9,75,75)
    #frame = cv2.Laplacian(frame,cv2.CV_8U)*8
    #gauss = cv2.GaussianBlur(frame,(1,1),0)
    #frame = cv2.Canny(frame, 60, 250)

    median = cv2.bilateralFilter(cv2.warpPerspective(hsv,M,(1280,960)),9,75,75)
    median = cv2.copyMakeBorder(median,50,50,50,50,cv2.BORDER_CONSTANT,value=(0,0,0))
    median = cv2.morphologyEx(median, cv2.MORPH_CLOSE, kernel,iterations=1)
    if demo:
        print("On a seperate copy of the original image in the HSV space:")
        print("- Did the same perspective change.")
        print("- Performed a bilateral filter on the image.")
        print("- Performed a morphological opening on the image.")
        cv2.imshow('Image',median)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("morph-2.jpg", median)
    outimg, argmax = argmax_label(median)
    outimg = cv2.cvtColor(outimg, cv2.COLOR_RGB2BGR)
    if demo:
        print("- Acquired the material labeling of the image.")
        print("- Acquired a \'pretty\' display image.")
        cv2.imshow('Image',outimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("mat.jpg", outimg)
    coin_mask = ((argmax==4)+(argmax==7))*255

    #ret,thresh1 = cv2.threshold(frame,100,255,cv2.THRESH_BINARY)
    #morph = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel,iterations=1)
    #ret,thresh1 = cv2.threshold(frame,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    circles = cv2.HoughCircles(frame,cv2.HOUGH_GRADIENT,1,50,
                            param1=50,param2=30,minRadius=30,maxRadius=100)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    value = 0
    if not type(circles) == type(None):
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            #Process
            feautures = feauture_extract(i,circles,argmax)
            classification = clf.predict([feautures])
            val = value_map(classification)
            value += val
            if val > 0:
                # draw the outer circle
                cv2.circle(outimg,(i[0],i[1]),i[2],(255,255,255),2)
                # draw the center of the circle
                cv2.circle(outimg,(i[0],i[1]),2,(0,0,255),3)
                cv2.putText(outimg,"R{0:.1f}".format(val),(i[0]-30,i[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
            else:
                # draw the outer circle
                cv2.circle(outimg,(i[0],i[1]),i[2],(100,100,100),2)


    #frame = cv2.bilateralFilter(frame,9,75,75)
    #print(hsv)
    #print(hsv.reshape(-1,3))

    #out = cv2.bitwise_and(coin_mask.astype(np.uint8),morph)
    #morph = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel,iterations=1)
    #outimg += frame
    #print(results.shape)
    #cv2.copyMakeBorder(cv2.warpPerspective(img,M,(1280,960)),50,50,50,50,cv2.BORDER_CONSTANT,value=BLACK)
    if demo:
        print("- Performed the hough transform on the first image.")
        print("For each circle:")
        print("* Extracted features using the circle position, radius, and material labels.")
        print("* Classified the circle using the feautures using a trained random forest (10 trees).")
        print("* Label the output image with the circle, indicating the position, radius and value")
        print("- Sum the value from each coin and return the image and value.")
        cv2.imwrite("outimg.jpg", outimg)
    return outimg, round(value,2), circles, argmax, cv2.copyMakeBorder(cv2.warpPerspective(img,M,(1280,960)),50,50,50,50,cv2.BORDER_CONSTANT,value=(0,0,0))

if __name__ == "__main__":
    main_detect()
