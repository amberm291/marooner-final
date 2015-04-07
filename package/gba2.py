#!/usr/bin/env python


import numpy as np
import cv2
import sys


if len(sys.argv) == 2:
    filename = sys.argv[1] # for drawing purposes
else:
    exit(0)

img = cv2.imread(filename)
img2 = img.copy()                               # a copy of original image
mask = np.zeros(img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG
output = np.zeros(img.shape,np.uint8)           # output image to be shown

rect_or_mask = 0
shiftx = 100
shifty = 50

rect = (0, 0, img.shape[0], img.shape[1])
print rect
#rect = (4, 7, 485, 643)

x = int(raw_input())
iterations=x
while(x >= 0):
    if (rect_or_mask == 0):         # grabcut with rect
        bgdmodel = np.zeros((1,65),np.float64)
        fgdmodel = np.zeros((1,65),np.float64)
        cv2.grabCut(img2,mask,rect,bgdmodel,fgdmodel,1,cv2.GC_INIT_WITH_RECT)
        rect_or_mask = 1
    elif rect_or_mask == 1:         # grabcut with mask
        bgdmodel = np.zeros((1,65),np.float64)
        fgdmodel = np.zeros((1,65),np.float64)
        cv2.grabCut(img2,mask,rect,bgdmodel,fgdmodel,1,cv2.GC_INIT_WITH_MASK)

    mask2 = np.where((mask==1) + (mask==3),255,0).astype('uint8')
    output = cv2.bitwise_and(img2,img2,mask=mask2)
    x = x - 1
    print "iteration:", iterations-x

cv2.imwrite("output.png", output)