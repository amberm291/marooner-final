import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[2],1)
img3 = img

L = int(raw_input())
R = int(raw_input())

startpix = []
endpix = []
startpix2 = []
endpix2 = []


"""for j in range(0, img.shape[1]):
	for i in range(0, img.shape[0]):
		if(img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2]):
			startpix.append(i)
			break
for j in range(0, img.shape[1]):
	for i in range(startpix[j],img.shape[0]):
		if(img[i][j][0]==img[0][0][0] and img[i][j][1]==img[0][0][1] and img[i][j][2]==img[0][0][2]):
			endpix.append(i-1)
			break
		if(i==img.shape[0]-1):
			endpix.append(i)

for j in range(0, img2.shape[1]):
	for i in range(0, img2.shape[0]):
		if(img2[i][j][0]!=img2[0][0][0] or img2[i][j][1]!=img2[0][0][1] or img2[i][j][2]!=img2[0][0][2]):
			startpix2.append(i)
			break

for j in range(0, img2.shape[1]):
	for i in range(startpix2[j],img2.shape[0]):
		if(img2[i][j][0]==img2[0][0][0] and img2[i][j][1]==img2[0][0][1] and img2[i][j][2]==img2[0][0][2]):
			endpix2.append(i-1)
			break
		if(i==img2.shape[0]-1):
			endpix2.append(i)"""

startU = 0
startP = 0
endU = 0
endP = 0
for j in range(0, img.shape[1]):
	startpix.append(0)
	endpix.append(0)
	cnt = 0
	for i in range(0, img.shape[0]):
		if(cnt == 0 and (img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2])):
			if(startU == 0):
				startU = j
			startpix[j]=i
			cnt = 1
		elif(cnt == 1 and (img[i][j][0]==img[0][0][0] or img[i][j][1]==img[0][0][1] or img[i][j][2]==img[0][0][2])):
			endpix[j]=i
			endU = j
			break

for j in range(0, img2.shape[1]):
	startpix2.append(0)
	endpix2.append(0)
	cnt = 0
	for i in range(0, img2.shape[0]):
		if(cnt == 0 and (img2[i][j][0]!=img2[0][0][0] or img2[i][j][1]!=img2[0][0][1] or img2[i][j][2]!=img2[0][0][2])):
			if(startP == 0):
				startP = j
			startpix2[j]=i
			cnt = 1
		elif(cnt == 1 and (img2[i][j][0]==img2[0][0][0] or img2[i][j][1]==img2[0][0][1] or img2[i][j][2]==img2[0][0][2])):
			endpix2[j]=i
			endP = j
			break
#R = 0
#L = img.shape[1]-1

for j in range(startU, endU):
	if(j +startP - startU >  endP):
		break
		for i in range((startpix[j]+endpix[j])/2,startpix[j]-1,-1):
			img3[i][j] = img2[(startpix2[j+startP-startU]+endpix2[j+startP-startU])/2+i-(startpix[j]+endpix[j])/2][j]
		for i in range((startpix[j]+endpix[j])/2,endpix[j]+1):
			img3[i][j] = img2[(startpix2[j+startP-startU]+endpix2[j+startP-startU])/2+i-(startpix[j]+endpix[j])/2][j]

cv2.imwrite("armFit" + sys.argv[1], img3)
