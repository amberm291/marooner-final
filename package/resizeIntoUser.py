import cv2
import numpy as np
import sys
import Queue

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[2],1)
ratio=float(raw_input())
ratio = 1 + ratio
#print ratio
#img2 = cv2.resize(img2, None, fx = 1/ratio, fy = 1/ratio, interpolation = cv2.INTER_AREA)
img2 = cv2.resize(img2, (int(ratio*img.shape[1]), int(ratio*img.shape[0])),interpolation = cv2.INTER_AREA)
h,w = img2.shape[:2]
q = Queue.Queue()
v = [[0 for x in xrange(w)] for x in xrange(h)]
q.put([0,0])
q.put([h-1,w-1])
q.put([0, w-1])
q.put([h-1,0])
q.put([0, w/2])
q.put([h-1, w/2])
while not q.empty():
	a,b = q.get()
	img2[a][b][0]=0
	img2[a][b][1]=0
	img2[a][b][2]=0
	for i in range(-1,2):
		for j in range(-1,2):
			if(i==0 and j==0):
				continue
			if((a+i)>=0 and (b+j)>=0 and (a+i)<h and (b+j)<w and v[a+i][b+j]==0 and img2[a+i][b+j][0]==0 and img2[a+i][b+j][1]==0 and img2[a+i][b+j][2]==0):
				q.put([a+i,b+j])
				v[a+i][b+j]=1
for i in range(img2.shape[0]):
	for j in range(img2.shape[1]):
		if(v[i][j]==0 and img2[i][j][0]==0 and img2[i][j][1]==0 and img2[i][j][2]==0):
			img2[i][j][0]=1
cv2.imwrite("resized" + sys.argv[2], img2)