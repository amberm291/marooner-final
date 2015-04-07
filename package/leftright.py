'''import cv2
import numpy as np
import sys
img = cv2.imread(sys.argv[1],1)
h = img.shape[0]
w = img.shape[1]
check = 0
L = 0
R = 0
H = 0
margin = 5
for j in range(0, w):
	for i in range(0, h):
		if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
			H = i
			check = 1
			break
	if(check == 1):
		break
oldPixBelH = 0
decStart = 0
for j in range(0, w, margin):
	newPixBelH = 0
	for i in range(H, h):
		if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
			newPixBelH = newPixBelH + 1
	if(newPixBelH > oldPixBelH):
		if(decStart == 0):
			oldPixBelH = newPixBelH
		else:
			L = j
			break;
	else:
		decStart = 1
check = 0
for j in range(w-1, -1, -1):
	for i in range(0, h):
		if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
			H = i
			check = 1
			break
	if(check == 1):
		break
oldPixBelH = 0
decStart = 0
for j in range(w-1, -1, -margin):
	newPixBelH = 0
	for i in range(H, h):
		if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
			newPixBelH = newPixBelH + 1
	if(newPixBelH > oldPixBelH):
		if(decStart == 0):
			oldPixBelH = newPixBelH
		else:
			R = j
			break;
	else:
		decStart = 1
img2 = img
for i in range(0, h):
	for j in range(0, w):
		if(j == L or j == R):
			img[i][j][0]=0
			img[i][j][1]=0
			img[i][j][2]=0
print L
print R
cv2.imwrite("segments1" + sys.argv[1], img2)
'''
import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
h = img.shape[0]
w = img.shape[1]

check = 0

L = 0
R = 0
H = 0
margin = 5

i=img.shape[0]/2
for j in range(0, img.shape[1]):
        if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
                L = j
                check = 1
                break


for j in range(img.shape[1]-1, -1, -1):
        if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
                R = j
                check = 1
                break


img2 = img


for i in range(0, h):
	for j in range(0, w):
		if(j == L or j == R):
			img[i][j][0]=0
			img[i][j][1]=0
			img[i][j][2]=0

print L
print R

cv2.imwrite("segments1" + sys.argv[1], img2)
