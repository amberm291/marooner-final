import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],0)
h = img.shape[0]
w = img.shape[1]

check = 0

L = 0
R = 0
T = 0
B = 0

for j in range(0, w):
	for i in range(0, h):
		if(img[i][j] != img[0][0]):
			L = j
			check = 1
			break
	if(check == 1):
		break

check = 0

for j in range(w-1, -1, -1):
	for i in range(0, h):
		if(img[i][j] != img[0][0]):
			R = j
			check = 1
			break
	if(check == 1):
		break

check = 0

for i in range(h-1, -1, -1):
	for j in range(0, w):
		if(img[i][j] != img[0][0]):
			B = i
			check = 1
			break
	if(check == 1):
		break
check = 0

for i in range(0, h):
	for j in range(0, w):
		if(img[i][j] != img[0][0]):
			T = i
			check = 1
			break
	if(check == 1):
		break



img2 = cv2.imread(sys.argv[1],1)
#img3 = np.zeros((B-T+1, R-L+1, 3))

print T
print L
print R
print B

crop_img = img2[T:B, L:R]
"""
for i in range(0, B-T+1):
	for j in range(0, R-L+1):
		for k in range(0, 3):
			img3[i][j][k] = img2[T+i][L+j][k]
"""
cv2.imwrite("cropped"+sys.argv[1], crop_img)