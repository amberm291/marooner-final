import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[2],1)
img_ = cv2.imread(sys.argv[1],1)
img2_ = cv2.imread(sys.argv[2],1)

LU = input()
RU = input()
LP = input()
RP = input()


for i in range(LU+1, img.shape[1]):
	for j in range(0, img.shape[0]):
		img[j][i][0] = 0
		img[j][i][1] = 0
		img[j][i][2] = 0

cv2.imwrite("leftUser.png", img)

for i in range(0, RU):
	for j in range(0, img_.shape[0]):
		img_[j][i][0] = 0
		img_[j][i][1] = 0
		img_[j][i][2] = 0

cv2.imwrite("rightUser.png", img_)

for i in range(LP+1, img2.shape[1]):
	for j in range(0, img2.shape[0]):
		img2[j][i][0] = 0
		img2[j][i][1] = 0
		img2[j][i][2] = 0

cv2.imwrite("leftProduct.png", img2)

for i in range(0, RP):
	for j in range(0, img2_.shape[0]):
		img2_[j][i][0] = 0
		img2_[j][i][1] = 0
		img2_[j][i][2] = 0

cv2.imwrite("rightProduct.png", img2_)