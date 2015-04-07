import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],0)
img3 = cv2.imread(sys.argv[1],1)
h = img.shape[0]
w = img.shape[1]

for j in range(0, w):
	for i in range(0, h):
		if(img[i][j] == 0):
			img3[i][j] = [0,0,3]

cv2.imwrite("blackPxRemoved.png", img3)
