import argparse
import cv2
import numpy as np
from helper import sub_frame

parser = argparse.ArgumentParser(description='Extract subs from silent films.')
parser.add_argument('-i','--input', nargs='+',required=True,help='Input video')
args = parser.parse_args()

input_files = args.input
for input_file in input_files:

    frame_no = 0
    frame = -1
    gray = -1
    bright = -1
    marked = []
    images = []
    mark_start = -1
    ticker = 0

    cap = cv2.VideoCapture(input_file)
    while(cap.isOpened()):
        last = gray
        last_bright = bright
        ret, frame = cap.read()
        if not ret:
            break
        frame_no += 1
        #print('Frame No:',frame_no)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #gray = cv2.convertScaleAbs(gray*d)
        #print(gray)
        #min_g = 50
        #max_g = 230
        #gray = (gray - min_g)*((255)/(max_g-min_g))
        #blur = cv2.GaussianBlur(gray,(5,5),0)
        ret3,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        kernel = np.ones((4,12),np.uint8)
        #kernel = np.identity(16,np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        #gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
        #gray = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=1)
        #gray = cv2.resize(gray, (40, 30))

        sided = np.concatenate((morph, gray), axis=1)
        #cv2.imshow('frame',sided)
        if frame_no > 1:

            #mse br
            #===================================
            #mse = sub_frame.mse(last,gray)
            #bright = max(np.average(frame),1)
            #if bright > last_bright:
            #    br = bright/(last_bright**2)
            #    mse_br = mse*br*(1+(bright-last_bright))
            #else:
            #    br = last_bright/(bright**2)
            #    mse_br = mse*br*(1+(last_bright-bright))


            bright = np.average(morph)
            #mse_sc = sub_frame.mse(last,gray)
            #if bright > last_bright:
            #    br = bright/(max(last_bright+bright,1)**2)
            #    mse_br = mse_sc*br
            #else:
            #    br = last_bright/(max(last_bright+bright,1)**2)
            #    mse_br = mse_sc*br
            #mse_br = mse_sc*(abs(bright-last_bright)/max(bright+last_bright,1))

            #error = sub_frame.sum_error(last,gray)
            #bright_e = sub_frame.bright_change(last,gray)
            #bright_ratio = sub_frame.bright_ratio(last,gray)
            #scaled_psnr = sub_frame.ratio_scaled_psnr(last,gray)
            #print('MSE*br:',mse_br)
            #print('Error:',error)
            #print('Bright Change:',bright_e)
            #print('Bright Ratio:',bright_ratio)
            #print('Brightness',bright)
            #print('Scaled MSE:',mse_sc)

            if frame_no%1000 == 0:
                print("Frame:",frame_no)

            ticker -= 1
            if bright < 2:
                #Start of block
                if ticker < 0:
                    mark_start = frame_no
                    image_set = [gray]
                    #brights = [np.average(gray)]
                else:
                    image_set += [gray]
                    #brights += [np.average(gray)]
                ticker = 5
                #join = np.concatenate((last, gray), axis=1)
                #cv2.imwrite( "transition{}-{}.jpg".format(frame_no,bright),last)
            elif ticker == 0:

                #rows = frame.shape[0]
                #cols = frame.shape[1]
                #a = cv2.getGaussianKernel(cols,200)
                #b = cv2.getGaussianKernel(rows,200)
                #c = b*a.T
                #d = c/c.max()

                marked += [(mark_start,frame_no-5)]
                #setting = np.argmax(brights)
                no_images = len(image_set)
                images += [np.concatenate((image_set[0], image_set[int(no_images/2)-1], image_set[no_images-1]), axis=1)]
                #vig = image_set[setting]*d
                #vig = cv2.convertScaleAbs(vig*(10/brights[setting]))
                #sobelx = cv2.convertScaleAbs(cv2.Sobel(vig,cv2.CV_64F,1,0,ksize=5))
                #ret4,thr_sob = cv2.threshold(sobelx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                #cv2.imwrite("transition{}.jpg".format(frame_no-5),thr_sob)
                #print(marked)

            #if scaled_psnr > 500:
            #    marked += [frame_no]
                #join = np.concatenate((last, gray), axis=1)
                #cv2.imwrite( "transition{}.jpg".format(frame_no), join)

        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
        #input('')

    #print('hi')
    for i in range(len(marked)):
        item = marked[i]
        image = cv2.resize(images[i], (960, 240))
        cv2.imshow('Frames {} - {}'.format(item[0],item[1]),image)
        cv2.waitKey(0)
        answer = input("Is this a valid intertitle? (y/n): ")
        cv2.destroyAllWindows()
        print(answer)

    cap.release()
    cv2.destroyAllWindows()
