import cv2
import numpy as np
import sys
import math

img = cv2.imread(sys.argv[1], 1)

h = img.shape[0]
w = img.shape[1]

for i in range(0,h):
	for j in range(0, w):
		if(img[i][j][0]==0 and img[i][j][1] == 0 and img[i][j][2] == 0):
			img[i][j][2] = 255

cv2.imwrite("debug.png", img)