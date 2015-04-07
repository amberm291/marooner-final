import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
h = img.shape[0]
w = img.shape[1]

check = 0

L = 0
R = 0

prevI = 0
prevJ = 0
start = -1
for i in range(img.shape[0]/2, -1, -1):
	cnt=start
	for j in range(img.shape[1]/2, -1, -1):
		if((cnt == 1) and (img[i][j][0] != 0 or img[i][j][1] != 0 or img[i][j][2] != 0)):
			cnt = 2
			start = 0
			prevI = i
			prevJ = j
			break
		if(cnt == start and (img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 0)):
			cnt = 1
	if(cnt == 1 and start != -1):
		break

prevJ2 = 0
prevI2 = 0
start = -1
for i in range(img.shape[0]/2, -1, -1):
	cnt=start
	for j in range(img.shape[1]/2, img.shape[1]):
		if((cnt == 1) and (img[i][j][0] != 0 or img[i][j][1] != 0 or img[i][j][2] != 0)):
			cnt = 2
			start = 0
			prevI2 = i
			prevJ2 = j
			break
		if(cnt == start and (img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 0)):
			cnt = 1
	if(cnt == 1 and start != -1):
		break

count = count2 = 0

i = prevI
j = prevJ
while(i>=0 and j >=0 and (img[i][j][0]!=0 or img[i][j][1]!=0 or img[i][j][2]!=0)):
	count+=1
	i-=1
	j-=1


i = prevI2
j = prevJ2
while(i>=0 and j < w and (img[i][j][0]!=0 or img[i][j][1]!=0 or img[i][j][2]!=0)):
	count2+=1
	i-=1
	j+=1

count-=1
count2-=1

start=0
for i in range(prevI, img.shape[0]):
	cnt=start
	if(img[i][w/2][0] == 0 and img[i][w/2][1] == 0 and img[i][w/2][2]==0):
		continue;
	for j in range(img.shape[1]/2, -1, -1):
		if((cnt == 1) and (img[i][j][0] != 0 or img[i][j][1] != 0 or img[i][j][2] != 0)):
			temp = count
			count-=0.1
			x=i
			y=j
			while(temp>0 and x>=0 and y >= 0):
				img[x][y][0] = img[h/2][w/2][0]
				img[x][y][1] = img[h/2][w/2][1]
				img[x][y][2] = img[h/2][w/2][2]
				x-=1
				y-=1
				temp-=1
			break
		if(cnt == start and (img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 0)):
			cnt = 1

start=0
for i in range(prevI2, img.shape[0]):
	cnt=start
	if(img[i][w/2][0] == 0 and img[i][w/2][1] == 0 and img[i][w/2][2]==0):
		continue;
	for j in range( img.shape[1]/2 , img.shape[1]):
		if((cnt == 1) and (img[i][j][0] != 0 or img[i][j][1] != 0 or img[i][j][2] != 0)):
			temp = count2
			count2-=0.1
			x=i
			y=j
			while(temp>0 and x>=0 and y < w):
				img[x][y][0] = img[h/2][w/2][0]
				img[x][y][1] = img[h/2][w/2][1]
				img[x][y][2] = img[h/2][w/2][2]
				x-=1
				y+=1
				temp-=1
			break
		if(cnt == start and (img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 0)):
			cnt = 1

kernel = np.ones((3,3),np.uint8)
img=cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
cv2.imwrite("arm.png", img)
