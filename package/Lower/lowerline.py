import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img3 = img

length = []
ind=0
flag=0

for i in range((2*img.shape[0])/3,0,-1):
        ct=0
	for j in range(1, img.shape[1]):
                if((img[i][j-1][0]!=img[0][0][0] or img[i][j-1][1]!=img[0][0][1] or img[i][j-1][2]!=img[0][0][2]) and (img[i][j][0]==img[0][0][0] and img[i][j][1]==img[0][0][1] and img[i][j][2]==img[0][0][2])):
                        ct=ct+1
        j=img.shape[1]
        if(img[i][j-1][0]!=img[0][0][0] or img[i][j-1][1]!=img[0][0][1] or img[i][j-1][2]!=img[0][0][2]):
                ct=ct+1
	if(ct==1):
		ind=i
		break

print ind
for i in range(0, img.shape[1]):
	img3[ind][i]=img3[0][0]
cv2.imwrite("lowerline"+sys.argv[1]+".png", img3)
