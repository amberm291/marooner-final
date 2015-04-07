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

print T
print L
print B
print R


img2 = img

for i in range(0, h):
	img2[i][L] = 255
	img2[i][R] = 255

for i in range(0, w):
	img2[T][i] = 255
	img2[B][i] = 255

cv2.imwrite("box.png", img2)
