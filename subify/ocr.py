import cv2
import numpy as np
from sklearn.cluster import KMeans

class liam_ocr:
    @staticmethod
    def binarize(image_in):
        gray = cv2.cvtColor(image_in, cv2.COLOR_BGR2GRAY)
        #inv = 255-gray
        #ret3,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

        mask = np.zeros((image_in.shape[0]+2, image_in.shape[1]+2), np.uint8)
        seed = 2
        while thresh[seed][2] == 0:
            seed += 2
        cv2.floodFill(thresh, mask, (seed,2), (0))

        #kernel = np.ones((4,12),np.uint8)
        #morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        #morph2 = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

        inv = 255-gray
        thresh2 = 255-cv2.adaptiveThreshold(inv,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)

        #img_final = np.maximum((thresh + thresh2)-255,np.zeros((image_in.shape[0], image_in.shape[1]), np.uint8))
        img_final = cv2.bitwise_and(thresh,thresh2)
        #kernel = np.ones((4,4),np.uint8)
        #morph = cv2.morphologyEx(img_final, cv2.MORPH_CLOSE, kernel)

        return img_final

    @staticmethod
    def lineSegmentation(binary):
        #Get horizontal segments
        hist = np.sum(binary, axis=1).astype(np.float) / binary.shape[1]
        segments = []
        thresh_x = 4
        seeking = False
        seg_start = 0
        seg_end = 0
        for i in range(len(hist)):
            if hist[i] > thresh_x:
                if seeking:
                    seg_end += 1
                else:
                    seeking = True
                    seg_start = i
                    seg_end = i
            else:
                if seeking:
                    seeking = False
                    segments += [(seg_start,seg_end+1)]
        if seeking:
            segments += [(seg_start,len(hist))]
        return segments

    @staticmethod
    def charSegmentation(binary,line):
        #Rough segmentation
        thresh_y = 4
        hor_hist = np.sum(binary[line[0]:line[1]][:], axis=0).astype(np.float) / (line[1]-line[0])
        line_segs = []
        seeking = False
        seg_start = 0
        seg_end = 0
        for x in range(len(hor_hist)):
            if hor_hist[x] > thresh_y:
                if seeking:
                    seg_end += 1
                else:
                    seeking = True
                    seg_start = x
                    seg_end = x
            else:
                if seeking:
                    seeking = False
                    line_segs += [(seg_start,seg_end+1)]
        if seeking:
            line_segs += [(seg_start,len(hor_hist))]
        return line_segs

    @staticmethod
    def charFineSegmentation(binary,char_vert,char_hor,min_vol):
        if (char_vert[1]-char_vert[0])*(char_hor[1]-char_hor[0]) == 0:
            return []
        #Internal segmentation
        line_segs = []
        subpic = binary[char_vert[0]:char_vert[1],char_hor[0]:char_hor[1]]
        ret, markers = cv2.connectedComponents(subpic)
        count = ret-1
        if count == 1:
            if np.sum(markers) < min_vol:
                return []
            vert_new, hor_new = liam_ocr.simpleCrop(subpic)
            new_subpic = subpic[vert_new[0]:vert_new[1],hor_new[0]:hor_new[1]]
            vert_fin = (vert_new[0]+char_vert[0],vert_new[1]+char_vert[0])
            hor_fin = (hor_new[0]+char_hor[0],hor_new[1]+char_hor[0])
            line_segs += [{'vert':vert_fin,'hor':hor_fin,'subpic':new_subpic}]
            #liam_ocr.simpleGrow(binary,vert_fin,hor_fin)
            #line_segs += [liam_ocr.simpleGrow(binary,char_vert,char_hor)]
        else:
            #see which contiguous regions are valid
            sub_segs = []
            for possib in range(1,count+1):
                #print(markers==possib)
                #print(min_vol)
                if np.sum(markers==possib) < min_vol:
                    #Invalid
                    continue
                else:
                    vert_new,hor_new = liam_ocr.simpleCrop(markers==possib)
                    subpic_crop = ((markers==possib)*255).astype(np.uint8)[vert_new[0]:vert_new[1],hor_new[0]:hor_new[1]]
                    vert_fin = (vert_new[0]+char_vert[0],vert_new[1]+char_vert[0])
                    hor_fin = (hor_new[0]+char_hor[0],hor_new[1]+char_hor[0])
                    #sub_segs += [liam_ocr.simpleGrow(binary,vert_fin,hor_fin)]
                    sub_segs += [{'vert':vert_fin,'hor':hor_fin,'subpic':subpic_crop}]
            line_segs += sub_segs
        return line_segs

    @staticmethod
    def simpleCrop(binary_in):
        if binary_in.max() == 0:
            return (0,0),(0,0)
        #Top
        start = 0
        while (np.sum(binary_in[start,:]) == 0):
            start += 1
        new_top = start
        #Bottom
        start = binary_in.shape[0]-1
        while np.sum(binary_in[start,:]) == 0:
            start -= 1
        new_bottom = start+1
        #Left
        start = 0
        while np.sum(binary_in[:,start]) == 0:
            start += 1
        new_left = start
        #Right
        start = binary_in.shape[1]-1
        while np.sum(binary_in[:,start]) == 0:
            start -= 1
        new_right = start+1

        return (new_top,new_bottom),(new_left,new_right)

    @staticmethod
    def simpleGrow(binary,win_y,win_x):
        inc = 20
        ret, markers = cv2.connectedComponents(binary[win_y[0]:win_y[1],win_x[0]:win_x[1]])
        #print binary[win_y[0]:win_y[1],win_x[0]:win_x[1]]
        #print(win_x,win_y)
        #print markers
        if ret == 1:
            if binary[win_x[0],win_y[0]] > 0:
                probable = 1
                probable_count = (win_x[1]-win_x[0])*(win_y[1]-win_y[0])
                certain_pos_x = 0
                certain_pos_y = 0
                markers = binary[win_y[0]:win_y[1],win_x[0]:win_x[1]] / 255
            else:
                return win_x, win_y, binary[win_y[0]:win_y[1],win_x[0]:win_x[1]]
        else:
            probable = 1
            probable_count = 0
            for i in range(1,ret):
                summed = np.sum(markers==i)
                if summed > probable_count:
                    probable_count = summed
                    probable = i
            certain = np.where(markers==probable)
            certain_pos_x = certain[0][0]
            certain_pos_y = certain[1][0]
        #print(certain_pos_x,certain_pos_y)
        size = probable_count
        size_prev = size - 20
        mark = probable
        win_x_old = win_x
        win_y_old = win_y
        mark = markers[certain_pos_x][certain_pos_y]
        markers[certain_pos_x][certain_pos_y] = -20
        #print(markers)
        markers[certain_pos_x][certain_pos_y] = mark
        while(size-size_prev > 0):
            win_x = (max(0,win_x[0]-inc),min(binary.shape[1],win_x[1]+inc))
            win_y = (max(0,win_y[0]-inc),min(binary.shape[1],win_y[1]+inc))
            mark_x = certain_pos_x + (win_x_old[0] - win_x[0])
            mark_y = certain_pos_y + (win_y_old[0] - win_y[0])
            #print(mark_y,mark_x)
            ret, markers = cv2.connectedComponents(binary[win_y[0]:win_y[1],win_x[0]:win_x[1]])
            mark = markers[mark_y][mark_x]
            #markers[mark_y][mark_x] = -20
            #print(markers)
            #markers[mark_y][mark_x] = mark
            size_prev = size
            size = np.sum(markers==mark)
        fin = ((markers==mark)*255).astype(np.uint8)
        #print(fin)
        (new_top,new_bottom),(new_left,new_right) = liam_ocr.simpleCrop(fin)
        #print fin[new_top:new_bottom,new_left:new_right]
        return {'vert':(new_top+win_y[0],new_bottom+win_y[0]),'hor':(new_left+win_x[0],new_right+win_y[0]),'subpic':fin[new_top:new_bottom,new_left:new_right]}
        #return (new_top+win_y[0],new_bottom+win_y[0]),(new_left+win_x[0],new_right+win_y[0]),fin[new_top:new_bottom,new_left:new_right]

    @staticmethod
    def wordSeperation(char_segs):
        if len(char_segs) <= 1:
            return [char_segs]
        if len(char_segs) == 2:
            return [char_segs]
        spaces = []
        tot = char_segs[0]['hor'][1]-char_segs[0]['hor'][0]
        for i in range(1,len(char_segs)):
            tot += char_segs[i]['hor'][1]-char_segs[i]['hor'][0]
            spaces += [char_segs[i]['hor'][0]-char_segs[i-1]['hor'][1]]
        avg = tot/len(char_segs)
        #print spaces
        #print char_segs
        X = np.array([spaces]).transpose()
        #print(X)
        kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
        #print(kmeans.cluster_centers_)

        #Sufficently similar?
        rat_min = 1.5
        #sufficiently big?
        gap_min = avg*0.2
        centres = (kmeans.cluster_centers_[0,0],kmeans.cluster_centers_[1,0])
        print(centres)
        space_ind = np.argmax(centres)
        space_gap = centres[space_ind]
        char_ind = 1 - space_ind
        char_gap = centres[char_ind]
        #space_gap = max(kmeans.cluster_centers_)
        #char_gap = min(kmeans.cluster_centers_)
        if (space_gap/char_gap > rat_min) & (space_gap > gap_min):
            #legitimate spaces
            labels = kmeans.labels_
            words = []
            new_word = [char_segs[0]]
            for i in range(1,len(char_segs)):
                if labels[i-1] == char_ind:
                    new_word += [char_segs[i]]
                else:
                    words += [new_word]
                    new_word = [char_segs[i]]
            words += [new_word]
        else:
            words = [char_segs]
        return words


    @staticmethod
    def characterSegmentation(binary):
        #ret, markers = cv2.connectedComponents(binary)
        #cv2.imshow(markers)
        #kernel = np.ones((4,12),np.uint8)
        #morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        #print hist
        segments = liam_ocr.lineSegmentation(binary)

        #Rough segmentation
        thresh_y = 4
        hor_segments = []
        #count = 0
        for line in segments:
            hor_segments += [liam_ocr.charSegmentation(binary,line)]
        #    count += len(hor_segments)
        #print(count)
        #Internal segmentation
        final_segs = []
        min_vol = (binary.shape[0]*0.005)**2
        for i in range(len(segments)):
            line_segs = []
            for j in range(len(hor_segments[i])):
                line_segs += liam_ocr.charFineSegmentation(binary,segments[i],hor_segments[i][j],min_vol)
            if len(line_segs) > 0:
                final_segs += [line_segs]

        #count = 0
        #for i in range(len(final_segs)):
        #    for j in range(len(final_segs[i])):
        #        count += 1
        #        cv2.imwrite("{}.png".format(count), final_segs[i][j]['subpic'])
        #start = 0
        #for i in range(len(segments)):
        #    seg = segments[i]
        #    binary[start:seg[0]-1][:] = 127
        #    start = seg[1]+1
        #binary[start:binary.shape[0]-1][:] = 127
        #count = 0
        #for i in range(len(final_segs)):
        #    count += len(final_segs[i])
        #print (len(segments),count)
        return final_segs

    @staticmethod
    def resCaptures(captures):
        print("Resizing")
        no_clusters = 80
        #For training, we just need the raw images.
        raws = []
        for segment in captures:
            for line in segment['final_segs']:
                for char in line:
                    #print(char)
                    res = np.array(cv2.resize(char['subpic'], (20,20))).astype(np.float)
                    res = (res / 255.0) - 0.5
                    #print(res)
                    raws += [res.flatten()]
        return raws
    @staticmethod
    def characterCluster(raws):
        #Resize all images to 20x20
        kmeans = KMeans(n_clusters=80, random_state=0).fit(raws)
