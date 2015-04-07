import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import Queue
img = cv2.imread(sys.argv[1],0)
img = cv2.Canny(img,10,100)
kernel = np.ones((9,9),np.uint8)
img=cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
img2 = cv2.imread(sys.argv[1],1)
h,w = img.shape[:2]
q = Queue.Queue()
p1 = img[0][0]
v = [[0 for x in xrange(w)] for x in xrange(h)]
q.put([0,0])
q.put([h-1,w-1])
q.put([0, w-1])
q.put([h-1,0])
q.put([0, w/2])
q.put([h-1, w/2])
while not q.empty():
	a,b = q.get()
	for i in range(a-1,a+2):
		for j in range(b-1,b+2):
			if(i>=0 and i<img.shape[0] and j>=0 and j<img.shape[1] and i!=a and j!=b and v[i][j]==0 and img[i][j]==p1):
				q.put([i,j])
				v[i][j]=1
for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		if(v[i][j]==1):
			img2[i][j][0]=0
			img2[i][j][1]=0
			img2[i][j][2]=0
cv2.imwrite("discretized.png",img2)
cv2.imwrite( "canny2.png", img)