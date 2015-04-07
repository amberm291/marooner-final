import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img3 = img

margin = 5
startpix = []
length = []

maxidx = 0
maxval = 0
for i in range(img.shape[0]/2, -1, -1):
	for j in range(img.shape[1]/2, img.shape[1]):
		if(img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 0):
			length.append(j)
			if(j>maxval):
				maxidx = i
				maxval = j
			break

H = maxidx

print H 

for i in range(0, img.shape[0]):
	for j in range(0, img.shape[1]):
		if(i == H):
			img3[i][j] = [0, 0, 0]
cv2.imwrite("armPitLine.png", img3)
