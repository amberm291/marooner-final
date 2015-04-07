import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[2],1)
img3 = img

startpix = []
length = []
startpix2 = []
length2 = []

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

for i in range(0, img2.shape[0]):
	for j in range(0, img2.shape[1]):
		if(img2[i][j][0]!=img2[0][0][0] or img2[i][j][1]!=img2[0][0][1] or img2[i][j][2]!=img2[0][0][2]):
			startpix2.append(j)
			break

for i in range(0, img2.shape[0]):
	for j in range(img2.shape[1]-1, -1, -1):
		if(img2[i][j][0]!=img2[0][0][0] or img2[i][j][1]!=img2[0][0][1] or img2[i][j][2]!=img2[0][0][2]):
			length2.append(j-startpix2[i])
			break

maxlen = length2[img.shape[0]/2]-length[img.shape[0]/2]
corri = 0
for i in range(img.shape[0]/2, img.shape[0]):
	if(maxlen < length2[i] - length[i]):
		maxlen = length2[i] - length[i]
		corri = i

#print 1.0*maxlen/img.shape[1]
print 0.2
