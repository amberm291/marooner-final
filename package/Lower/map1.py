import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[2],1)
img3 = img


startpix = [0 for i in range(img.shape[0])]
endpix = [0 for i in range(img.shape[0])]
startpix2 = [0 for i in range(img2.shape[0])]
endpix2 = [0 for i in range(img2.shape[0])]
first=0
for i in range(0, img.shape[0]):
	for j in range(0, img.shape[1]):
		if(img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2]):
			first=i
			break
	if(first!=0):
                break

for i in range(0, img.shape[0]):
	for j in range(0, img.shape[1]):
		if(img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2]):
			startpix[i]=j
			break
for i in range(0, img.shape[0]):
	for j in range(img.shape[1]-1,0,-1):
		if(img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2]):
			endpix[i]=j
			break
		if(j==0):
			endpix[i]=j

for i in range(0, img2.shape[0]):
	for j in range(0, img2.shape[1]):
		if(img2[i][j][0]!=img2[0][0][0] or img2[i][j][1]!=img2[0][0][1] or img2[i][j][2]!=img2[0][0][2]):
			startpix2[i]=j
			break

for i in range(0, img2.shape[0]):
	for j in range(img2.shape[1]-1,0,-1):
		if(img2[i][j][0]!=img2[0][0][0] or img2[i][j][1]!=img2[0][0][1] or img2[i][j][2]!=img2[0][0][2]):
			endpix2[i]=j
			break
		if(j==0):
			endpix2[i]=j
#R = 0
#L = img.shape[1]-1
line1 = int(raw_input())-1
line2 = int(raw_input())-1
for i in range(line2,first,-1):
	img2[line1+i-line2][(startpix2[i]+endpix2[i])/2]=img2[0][0]
	print startpix2[i],
	print endpix2[i]
	for j in range((startpix[i]+endpix[i])/2,startpix[i],-1):
		img3[i][j]=img2[line1+i-line2][(startpix2[line1+i-line2]+endpix2[line1+i-line2])/2+j-(startpix[i]+endpix[i])/2]
	for j in range((startpix[i]+endpix[i])/2,endpix[i]):
		img3[i][j]=img2[line1+i-line2][(startpix2[line1+i-line2]+endpix2[line1+i-line2])/2-j+(startpix[i]+endpix[i])/2]

cv2.imwrite("justchecking.png", img2)
cv2.imwrite("resultlower.png", img3)
