import cv2
import numpy as np
import sys
import Queue
import math
from math import *
if __name__ == '__main__':
	img = cv2.imread(sys.argv[1],1)
	img2 = cv2.imread(sys.argv[2],1)
	col=img2[floor(img2.shape[0]/2)][floor(img2.shape[1]/2)]
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
				if(i>=0 and i<img.shape[0] and j>=0 and j<img.shape[1] and i!=a and j!=b and v[i][j]==0 and img[i][j][0]==p1[0] and img[i][j][1]==p1[1] and img[i][j][2]==p1[2]):
					q.put([i,j])
					v[i][j]=1
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if(v[i][j]==0):
				img[i][j][0]=col[0]
				img[i][j][1]=col[1]
				img[i][j][2]=col[2]
	kernel = np.ones((5,5),np.uint8)
	closing=cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
	cv2.imwrite("mainOutput.png",closing)
