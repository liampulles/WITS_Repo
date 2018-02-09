import numpy as np
import cv2
from scipy.spatial.distance import cdist

class sub_frame:
    """Algorithms which work over the domain of a single frame."""
    def mse(frame1,frame2):
        #return np.average(cdist(frame1,frame2)**2)
        return np.average(np.square(np.subtract(frame2,frame1)))

    def psnr(frame1,frame2):
        mse_in = sub_frame.mse(frame1,frame2)
        if (mse_in == 0):
            return 0
        return (20*np.log10(255)) - (10*np.log(mse_in))

    def sum_error(frame1,frame2):
        return np.sum(np.subtract(frame2,frame1))

    def bright_change(frame1,frame2):
        return np.average(frame2)-np.average(frame1)

    def bright_ratio(frame1,frame2):
        return (np.average(frame2) + 1) / (np.average(frame1) + 1)

    def ratio_scaled_psnr(frame1,frame2):
        frame1_min = np.min(frame1)
        frame1_max = np.max(frame1)

        frame2_min = np.min(frame2)
        frame2_max = np.max(frame2)

        if frame1_max-frame1_min == 0:
            frame1_norm = frame1
        else:
            frame1_norm = (255/(frame1_max-frame1_min))*(frame1-frame1_min)
        if frame2_max-frame2_min == 0:
            frame2_norm = frame2
        else:
            frame2_norm = (255/(frame2_max-frame2_min))*(frame2-frame2_min)

        frame1_avg = np.average(frame1_norm)
        frame2_avg = np.average(frame2_norm)

        psnr_in = sub_frame.psnr(frame1_norm,frame2_norm)

        if frame1_avg > frame2_avg:
            br = (frame2_avg + 1)/(frame1_avg + 1)
        else:
            br = (frame1_avg + 1)/(frame2_avg + 1)
        #print("max:",np.max(frame1_norm),"min:",np.min(frame1_norm))
        return np.abs(psnr_in/(br**2))

class sub_file:
    """Algorithms which work over the domain of a single file."""
    @staticmethod
    def segment_find(input_file):
        frame_no = 0
        frame = -1
        gray = -1
        bright = -1
        marked = []
        images = []
        grays = []
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

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            ret3,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            kernel = np.ones((4,12),np.uint8)

            morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

            sided = np.concatenate((morph, gray), axis=1)
            #cv2.imshow('frame',sided)
            if frame_no > 1:

                bright = np.average(morph)

                if frame_no%1000 == 0:
                    print("Frame:",frame_no)

                ticker -= 1
                if bright < 2:
                    #Start of block
                    if ticker < 0:
                        mark_start = frame_no
                        #image_set = [frame]
                        #gray_set = [gray]
                        #brights = [np.average(gray)]
                    #else:
                        #image_set += [frame]
                        #gray_set += [gray]
                        #brights += [np.average(gray)]
                    ticker = 5
                    #join = np.concatenate((last, gray), axis=1)
                    #cv2.imwrite( "transition{}-{}.jpg".format(frame_no,bright),last)
                elif ticker == 0:

                    marked += [(mark_start,frame_no-5)]
                    #setting = np.argmax(brights)
                    #no_images = len(image_set)
                    #grays += [(gray_set)]
                    #images += [(image_set)]

        #for i in range(len(marked)):
            #item = marked[i]
            #image = cv2.resize(images[i], (960, 240))
            #cv2.imshow('Frames {} - {}'.format(item[0],item[1]),image)
            #cv2.waitKey(0)
            #answer = input("Is this a valid intertitle? (y/n): ")
            #cv2.destroyAllWindows()
            #print(answer)

        cap.release()
        cv2.destroyAllWindows()
        return marked
