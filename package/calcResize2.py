import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],0)
img2 = cv2.imread(sys.argv[2],0)

pixCountUser = 0
pixCountCat = 0

for j in xrange(img.shape[1]):
	if img[img.shape[0]-100][j] != 0:
		pixCountUser += 1

for j in xrange(img2.shape[1]):
	if img2[img2.shape[0]-100][j] != 0:
		pixCountCat += 1

print 0.3
#print float(abs(pixCountCat-pixCountUser))/float(img.shape[1]) 