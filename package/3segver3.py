import cv2
import numpy as np
import sys
import math

img = cv2.imread(sys.argv[1],1)
imgl = cv2.imread(sys.argv[2],1)
imgr = cv2.imread(sys.argv[3],1)

h=img.shape[0]
w=img.shape[1]
for i in range(h):
	for j in range(w):
		if(imgl[i][j][0]!=0 or imgl[i][j][1]!=0 or imgl[i][j][2]!=0):
			img[i][j]=imgl[i][j]
		if(imgr[i][j][0]!=0 or imgr[i][j][1]!=0 or imgr[i][j][2]!=0):
			img[i][j]=imgr[i][j]
cv2.imwrite(sys.argv[1],img)