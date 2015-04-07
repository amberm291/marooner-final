import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[2],1)
img3 = img

L = int(raw_input())
R = int(raw_input())
H = int(raw_input())
L = L + 40
R = R - 20
H = H - 5

startpix = []
endpix = []
startpix2 = []
endpix2 = []


for j in range(0, img.shape[1]):
	for i in range(0, img.shape[0]):
		if(img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2]):
			startpix.append(i)
			break
for j in range(0, img.shape[1]):
	for i in range(img.shape[0]-1, -1, -1):
		if(img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2]):
			endpix.append(i)
			break

for j in range(0, img2.shape[1]):
	for i in range(0, img2.shape[0]):
		if(img2[i][j][0]!=img2[0][0][0] or img2[i][j][1]!=img2[0][0][1] or img2[i][j][2]!=img2[0][0][2]):
			startpix2.append(i)
			break

for j in range(0, img2.shape[1]):
	for i in range(img2.shape[0]-1, -1, -1):
		if(img2[i][j][0]!=img2[0][0][0] or img2[i][j][1]!=img2[0][0][1] or img2[i][j][2]!=img2[0][0][2]):
			endpix2.append(i)
			break
R = 0
L = img.shape[1]-1

for j in range(0, img.shape[1]):
	if(j <= L or j >= R):
		for i in range(startpix[j], endpix[j]):
			if(i < H and startpix2[j]+i-startpix[j] < endpix2[j]):
				img3[i][j] = img2[startpix2[j]+i-startpix[j]][j]

cv2.imwrite("result3seg.png", img3)
