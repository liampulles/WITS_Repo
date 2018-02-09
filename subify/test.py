from ocr import liam_ocr
import cv2
import numpy as np

new = np.zeros((8, 8), np.uint8)
new[0:4,1:8] = 255
new[5:8,1:8] = 255
new[:,3] = 0
new[0,4] = 0
new[0,5] = 0
new[1,5] = 0
new[1,6] = 0
new[2,6] = 0
new[2,7] = 0
new[3,7] = 0

print(new)
segments = liam_ocr.lineSegmentation(new)
#print(segments)
hor_seg = liam_ocr.charSegmentation(new,segments[0])
#print(hor_seg)
print(liam_ocr.simpleGrow(new,(3,5),(2,3)))
