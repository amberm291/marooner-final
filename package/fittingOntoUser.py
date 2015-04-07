import cv2
import numpy as np
import sys
import time

img = cv2.imread(sys.argv[1], 1)
img2 = cv2.imread(sys.argv[2], 1)
T = int(raw_input())
L = int(raw_input())
R = int(raw_input())
B = int(raw_input())
h = img.shape[0]
w = img.shape[1]
for i in range(T, B):
	for j in range(L, R):
		if(img2[i-T][j-L][0] != 0 or img2[i-T][j-L][1] != 0 or img2[i-T][j-L][2] != 0):
			img[i][j] = img2[i-T][j-L]

outname = str(int(time.time())) + ".png"
print outname
#outname = sys.argv[3] + ".png"
cv2.imwrite(outname, img)