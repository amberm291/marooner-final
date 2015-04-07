import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import Queue

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[1],1)
img = cv2.Canny(img,10,175)

kernel = np.ones((3,3),np.uint8)
img = cv2.dilate(img,kernel)
kernel = np.ones((2,2),np.uint8)
img = cv2.erode(img,kernel)
cv2.imwrite('erode.png',img)

img_ = np.zeros((img.shape[0]+2,img.shape[1]+2))
img2_ = np.zeros((img.shape[0]+2,img.shape[1]+2,3))
for i in range(img.shape[0]+2):
	for j in range(img.shape[1]+2):
		if(i==0 or i==img.shape[0]+1 or j == 0 or j == img.shape[1]+1):
			img_[i][j] = img[0][0]
			img2_[i][j] = img2[0][0]
		else:
			img_[i][j] = img[i-1][j-1]
			img2_[i][j] = img2[i-1][j-1]
img = img_
img2 = img2_
h,w = img.shape[:2]
q = Queue.Queue()
p1 = img[0][0]
v = np.zeros((h,w))
q.put([0,0])
#q.put([h-1,w-1])
#q.put([0, w-1])
#q.put([h-1,0])
#q.put([0, w/2])
#q.put([h-1, w/2])
while not q.empty():
	a,b = q.get()
	img2[a][b] = [0,0,0]
	if a>0 and b>0 and v[a-1][b-1]==0:
		if img[a-1][b-1] == p1:
			q.put([a-1,b-1])
			v[a-1][b-1]=1
		else:
			img2[a-1][b-1] = [0,0,0]
	if a>0 and v[a-1][b]==0:
		if img[a-1][b] == p1:
			q.put([a-1,b])
			v[a-1][b]=1
		else:
			img2[a-1][b] = [0,0,0]
	if b>0 and v[a][b-1]==0:
		if img[a][b-1] == p1:
			q.put([a,b-1])
			v[a][b-1]=1
		else:
			img2[a][b-1] = [0,0,0]
	if a>0 and b<(w-1) and v[a-1][b+1]==0:
		if img[a-1][b+1] == p1:
			q.put([a-1,b+1])
			v[a-1][b+1]=1
		else:
			img2[a-1][b+1] = [0,0,0]
	if b<(w-1) and v[a][b+1]==0:
		if img[a][b+1] == p1:
			q.put([a,b+1])
			v[a][b+1]=1
		else:
			img2[a][b+1] = [0,0,0]
	if a<(h-1) and b<(w-1) and v[a+1][b+1]==0:
		if img[a+1][b+1] == p1:
			q.put([a+1,b+1])
			v[a+1][b+1]=1
		else:
			img2[a+1][b+1] = [0,0,0]
	if a<(h-1) and v[a+1][b]==0:
		if img[a+1][b] == p1:
			q.put([a+1,b])
			v[a+1][b]=1
		else:
			img2[a+1][b] = [0,0,0]
	if a<(h-1) and b>0 and v[a+1][b-1]==0:
		if img[a+1][b-1] == p1:
			q.put([a+1,b-1])
			v[a+1][b-1]=1
		else:
			img2[a+1][b-1] = [0,0,0]

img2_new = img2[1:img2.shape[0]-1][1:img2.shape[1]-1]
cv2.imwrite("floodOut.png",img2_new)
cv2.imwrite( "canny2.png", img)