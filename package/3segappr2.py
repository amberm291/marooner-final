
import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
h = img.shape[0]
w = img.shape[1]
img2 = img

check = 0

L = 0
R = 0

i=h/2
for j in range(w/2, -1, -1):
        if(img[i][j][0] == img[0][0][0] and img[i][j][1] == img[0][0][1] and img[i][j][2] == img[0][0][2]):
                L = j
                break


for j in range(w/2, w):
        if(img[i][j][0] == img[0][0][0] and img[i][j][1] == img[0][0][1] and img[i][j][2] == img[0][0][2]):
                R = j
                break
LPrev = L
RPrev = R

check = 0

L = 0
R = 0

prevI = 0
start = -1
for i in range(img.shape[0]/2, -1, -1):
	cnt=start
	for j in range(img.shape[1]/2, -1, -1):
		if((cnt == 1) and (img[i][j][0] != 0 or img[i][j][1] != 0 or img[i][j][2] != 0)):
			cnt = 2
			start = 0
			prevI = i
			break
		if(cnt == start and (img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 0)):
			cnt = 1
	if(cnt == 1 and start != -1):
		break


for j in range(img.shape[1]/2, -1, -1):
	if((img[prevI+1][j][0] == 0 and img[prevI+1][j][1] == 0 and img[prevI+1][j][2] == 0)):
		prevJ1 = j
		break

for j in range(img.shape[1]/2, -1, -1):
	if((img[prevI][j][0] == 0 and img[prevI][j][1] == 0 and img[prevI][j][2] == 0)):
		prevJ2 = j
		break

L = min(prevJ1, prevJ2)

prevI = 0
start = -1
for i in range(img.shape[0]/2, -1, -1):
	cnt=start
	for j in range(img.shape[1]/2, img.shape[1]):
		if((cnt == 1) and (img[i][j][0] != 0 or img[i][j][1] != 0 or img[i][j][2] != 0)):
			cnt = 2
			start = 0
			prevI = i
			break
		if(cnt == start and (img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 0)):
			cnt = 1
	if(cnt == 1 and start != -1):
		break


for j in range(img.shape[1]/2, img.shape[1]):
	if((img[prevI+1][j][0] == 0 and img[prevI+1][j][1] == 0 and img[prevI+1][j][2] == 0)):
		prevJ1 = j
		break

for j in range(img.shape[1]/2, img.shape[1]):
	if((img[prevI][j][0] == 0 and img[prevI][j][1] == 0 and img[prevI][j][2] == 0)):
		prevJ2 = j
		break

R = min(prevJ1, prevJ2)


if(abs(w/2-L)<abs(LPrev-L)):
	L = LPrev
if(abs(w/2-R)<abs(RPrev-R)):
	R = RPrev
if(abs(LPrev/2-L)<abs(LPrev-L)):
	L = LPrev
if(abs(RPrev + (w-RPrev)/2 - R)<abs(RPrev-R)):
	R = RPrev

for i in range(0, h):
	for j in range(0, w):
		if(j == L or j == R):
			img[i][j][0]=0
			img[i][j][1]=0
			img[i][j][2]=0

print L
print R

cv2.imwrite("segments1" + sys.argv[1], img2)