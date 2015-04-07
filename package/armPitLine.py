import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img3 = img

margin = 5
startpix = []
length = []

for i in range(0, img.shape[0]):
	for j in range(0, img.shape[1]):
		if(img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2]):
			startpix.append(j)
			break

for i in range(0, img.shape[0]):
	for j in range(img.shape[1]-1, -1, -1):
		if(img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2]):
			length.append(j-startpix[i])
			break

H = 0;
for i in range(img.shape[0]/2, -1, -1*margin):
	if(length[i] < length[i-margin]-10):
		H = i - (margin/2)
		print H
		break;

for i in range(0, img.shape[0]):
	for j in range(0, img.shape[1]):
		if(i == H):
			img3[i][j] = [0, 0, 0]
cv2.imwrite("armPitLine.png", img3)
