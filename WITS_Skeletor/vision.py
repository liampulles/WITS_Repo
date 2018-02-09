#This class provides functions to ascertain the state of the board.
from enum import Enum
import cv2
import numpy as np
from scipy import ndimage

class Color(Enum):
    #In RGB format
    YELLOW = (244, 241, 66)
    RED = (255, 33, 33)
    GREEN = (15, 224, 19)
    BLUE = (9, 18, 193)
    BLACK = (28, 28, 28)
    WHITE = (237, 237, 237)

class SkeletorVision:
    device = 1
    cap = None
    trans = None
    width = 400
    height = 400
    ref_pieces = None

    def mean_from_mask(self,mask):
        locs = np.where(mask > 128)
        locs = list(zip(locs[0],locs[1]))
        return np.mean(locs,axis=0)

    def scale_points(self,tl,tr,bl,br,scale):
        center = np.mean(np.vstack((tl,tr,bl,br)),axis=0)
        diff_s = 1.0 - scale
        diff_y = (center[0]-tl[0])*diff_s
        diff_x = (center[1]-tl[1])*diff_s
        tl += np.array([diff_y,diff_x])
        diff_y = (center[0]-tr[0])*diff_s
        diff_x = (center[1]-tr[1])*diff_s
        tr += np.array([diff_y,diff_x])
        diff_y = (center[0]-bl[0])*diff_s
        diff_x = (center[1]-bl[1])*diff_s
        bl += np.array([diff_y,diff_x])
        diff_y = (center[0]-br[0])*diff_s
        diff_x = (center[1]-br[1])*diff_s
        br += np.array([diff_y,diff_x])
        return np.vstack((tl,tr,bl,br))

    def calibrate(self):
        if self.connected():
            print("Calibrating...")
            ret, frame1 = self.getFrame()
            ret, frame2 = self.getFrame()
            ret, frame3 = self.getFrame()
            #print(frame1.shape)
            if ret:
                frame = frame1.astype(np.float64)+frame2.astype(np.float64)+frame2.astype(np.float64)
                frame = (frame/3.0).astype(np.uint8)
                #Find corners
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                #H1
                print("Getting H1...")
                startx = 42
                starty = 422
                endx = 94
                endy = 469
                crop_hsv = hsv[starty:endy,startx:endx,:]
                # define range of blue color in HSV
                lower_green = np.array([40,50,50])
                upper_green = np.array([60,255,255])
                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(crop_hsv, lower_green, upper_green)
                kernel = np.ones((5,5),np.uint8)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                h1_pos = ndimage.measurements.center_of_mass(mask)
                h1_pos += np.array([starty,startx])
                #A8
                print("Getting A8...")
                startx = 453
                starty = 0
                endx = 506
                endy = 45
                crop_hsv = hsv[starty:endy,startx:endx,:]
                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(crop_hsv, lower_green, upper_green)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                a8_pos = ndimage.measurements.center_of_mass(mask)
                a8_pos += np.array([starty,startx])
                #A1
                print("Getting A1...")
                startx = 51
                starty = 13
                endx = 93
                endy = 51
                crop_hsv = hsv[starty:endy,startx:endx,:]
                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(crop_hsv, lower_green, upper_green)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                a1_pos = ndimage.measurements.center_of_mass(mask)
                a1_pos += np.array([starty,startx])
                #H8
                print("Getting A8...")
                startx = 471
                starty = 429
                endx = 508
                endy = 466
                crop_hsv = hsv[starty:endy,startx:endx,:]
                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(crop_hsv, lower_green, upper_green)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                h8_pos = ndimage.measurements.center_of_mass(mask)
                h8_pos += np.array([starty,startx])
                #draw
                cv2.circle(frame, (int(h8_pos[1]),int(h8_pos[0])), 2, (0,0,255), -1)
                cv2.circle(frame, (int(a8_pos[1]),int(a8_pos[0])), 2, (0,0,255), -1)
                cv2.circle(frame, (int(h1_pos[1]),int(h1_pos[0])), 2, (0,0,255), -1)
                cv2.circle(frame, (int(a1_pos[1]),int(a1_pos[0])), 2, (0,0,255), -1)
                cv2.imshow('image',frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                #Transform to board corner spots
                print("Scaling...")
                scales = self.scale_points(a1_pos,a8_pos,h1_pos,h8_pos,0.91).astype(np.float32)
                scales = np.flip(scales,axis=1)
                dst = np.array([[0,0],[self.width,0],[0,self.height],[self.width,self.height]]).astype(np.float32)
                dst = np.flip(dst,axis=1)
                #print(dst)
                self.trans = cv2.getPerspectiveTransform(scales,dst)
                print("Storing pieces...")
                self.ref_pieces = dict()
                board = self.boardImage(frame)
                board = cv2.medianBlur(board, 3)
                for index in self.getIndices():
                    self.ref_pieces[index] = self.spaceImage(board,index)
                print("Calibrated.")
                return


    def openCamera(self):
        self.cap = cv2.VideoCapture(self.device)

    def closeCamera(self):
        self.cap.release()
        self.cap = None

    def getFrame(self):
        return self.cap.read()

    def connected(self):
        if self.cap == None:
            return False
        else:
            return True

    def detectPieces(self,frame,color):
        thresh = 200.0
        #Convert frame to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #Get difference image
        rgb = rgb - np.array(color)
        summed = np.sum(rgb**2,axis=2)**0.5

        #Get mask
        mask = (summed <= thresh)*255

    def boardImage(self,frame):
        return cv2.warpPerspective(frame,self.trans,(self.width,self.height))

    def spaceImage(self,board,piece):
        number = piece[1]
        letter = piece[0]
        xspace = board.shape[1]/8.0
        yspace = board.shape[0]/8.0
        xint = ord(piece[0].lower())-97
        yint = int(piece[1])-1
        xstart = int(xint*xspace)
        xend = int((xint+1)*xspace)
        ystart = int(yint*yspace)
        yend = int((yint+1)*yspace)
        #print(xint,yint)
        return board[ystart:yend,xstart:xend,:]

    def isFull(self,diff,index):
        #What is the variance?
        print(index,np.average(diff))
        if np.average(diff) > 15:
            return True
        else:
            return False
        #return np.average(piece,axis=(0,1))

    def getIndices(self):
        indices = ['a1','a3','a5','a7','b2','b4','b6','b8','c1','c3','c5','c7']
        indices += ['d2','d4','d6','d8','e1','e3','e5','e7','f2','f4','f6','f8']
        indices += ['g1','g3','g5','g7','h2','h4','h6','h8']
        return indices

    def centerPixel(self,image):
        if len(image.shape) == 2:
            return image[int(image.shape[0]/2),int(image.shape[1]/2)]
        if len(image.shape) == 3:
            return image[int(image.shape[0]/2),int(image.shape[1]/2),:]

    def getBoard(self):
        #Make sure we're connected
        if not self.connected():
            self.openCamera()
            if not self.connected():
                print("Unable to connect webcam")
                return False, None

        #Get frame
        ret, frame = self.getFrame()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        board = self.boardImage(frame)
        board = cv2.medianBlur(board, 3)
        #cv2.imshow('image',board)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #return
        count1 = 0
        count2 = 0
        variances = []
        for index in self.getIndices():
            #count2 += 1
            #if (count1+count2)%2 == 1:
            #    continue
            piece = self.spaceImage(board,index)
            diff1 = piece.astype(np.float64)-self.ref_pieces[index].astype(np.float64)
            diff1 = np.linalg.norm(diff1,axis=2)
            diff1 = np.clip((diff1-10.0)*4.0,0,255)
            if self.isFull(diff1,index):
            #    print(index,"is occupied")28
                print(np.max(np.max(diff1)),np.min(np.min(diff1)))
                #whities = np.where(diff >= 100.0)
                #diff = np.zeros(diff.shape,dtype=np.uint8)
                #diff[whities] = 255
                center = ndimage.measurements.center_of_mass(diff1)
                print(center/np.array(list(diff1.shape)))
                ret,diff = cv2.threshold(diff1.astype(np.uint8),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                #print(self.centerPixel(piece),self.centerPixel(self.ref_pieces[index]))
                cv2.imshow(index,diff)#.astype(np.uint8))
                print("showing",index)
                #cv2.imshow(index,piece)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            #cv2.imshow(index,self.ref_pieces[index])
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            #variances += [self.isFull(piece).tolist()]
        #print(np.array(variances))
        #piece2 = self.spaceImage(board,'f6')
        #self.isFull(piece1)
        #self.isFull(piece2)
        if not ret:
            print("Error in retrieveing frame from the webcam.")
            return False, None

        for color in [Color.YELLOW]:
            self.detectPieces(frame,color.value)

#For testing
if __name__ == "__main__":
    sv = SkeletorVision()
    sv.openCamera()
    sv.calibrate()
    #input('type to continue')
    sv.closeCamera()
    sv.openCamera()
    print(sv.getBoard())
