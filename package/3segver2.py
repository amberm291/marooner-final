import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[2],1)
img3 = img

L = int(raw_input())
R = int(raw_input())
L2 = int(raw_input())
R2 = int(raw_input())


startpix = []
endpix = []
startpix2 = []
endpix2 = []


for j in range(0, img.shape[1]):
	startpix.append(0)
	for i in range(0, img.shape[0]):
		if(img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2]):
			startpix[j]=i
			break
for j in range(0, img.shape[1]):
	for i in range(startpix[j],img.shape[0]):
		if(img[i][j][0]==img[0][0][0] and img[i][j][1]==img[0][0][1] and img[i][j][2]==img[0][0][2]):
			endpix.append(i-1)
			break
		if(i==img.shape[0]-1):
			endpix.append(i)

for j in range(0, img2.shape[1]):
	startpix2.append(0)
	for i in range(0, img2.shape[0]):
		if(img2[i][j][0]!=img2[0][0][0] or img2[i][j][1]!=img2[0][0][1] or img2[i][j][2]!=img2[0][0][2]):
			startpix2[j]=i
			break

for j in range(0, img2.shape[1]):
	for i in range(startpix2[j],img2.shape[0]):
		if(img2[i][j][0]==img2[0][0][0] and img2[i][j][1]==img2[0][0][1] and img2[i][j][2]==img2[0][0][2]):
			endpix2.append(i-1)
			break
		if(i==img2.shape[0]-1):
			endpix2.append(i)
#R = 0
#L = img.shape[1]-1

for j in range(0, img.shape[1]):
	if(j <= L or j >= R):
		for i in range((startpix[j]+endpix[j])/2,startpix[j]-1,-1):
			if((startpix2[j]+endpix2[j])/2+i-(startpix[j]+endpix[j])/2 >= startpix2[j]):
				img3[i][j] = img2[(startpix2[j]+endpix2[j])/2+i-(startpix[j]+endpix[j])/2][j]
		for i in range((startpix[j]+endpix[j])/2,endpix[j]+1):
			if((startpix2[j]+endpix2[j])/2+i-(startpix[j]+endpix[j])/2 < endpix2[j]):
				img3[i][j] = img2[(startpix2[j]+endpix2[j])/2+i-(startpix[j]+endpix[j])/2][j]
	'''
	if(j<=L):
		for i in range(startpix[j],endpix[j]+1):
			try:
				if(startpix2[j+L2-L]+i-startpix[j] >= startpix2[j+L2-L] and startpix2[j+L2-L]+i-startpix[j]<=endpix2[j+L2-L]):
					img3[i][j] = img2[startpix2[j+L2-L]+i-startpix[j]][j+L2-L]
			except:
				pass
	if(j>=R):
		for i in range(startpix[j],endpix[j]+1):
			try:
				if(startpix2[j+R2-R]+i-startpix[j] >= startpix2[j+R2-R] and startpix2[j+R2-R]+i-startpix[j]<=endpix2[j+R2-R]):
					img3[i][j] = img2[startpix2[j+R2-R]+i-startpix[j]][j+R2-R]
			except:
				pass'''
cv2.imwrite("result3seg.png", img3)
