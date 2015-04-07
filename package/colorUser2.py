import cv2
import numpy as np 
import math
import sys
from math import *
import Queue

if __name__ == '__main__':
	img = cv2.imread(sys.argv[1],0)
	img3 = cv2.imread(sys.argv[1],1)
	img2 = cv2.imread(sys.argv[2],1)
	col = img2[floor(img2.shape[0]/2)][floor(img2.shape[1]/2)]
	h,w = img.shape[:2]
	p1 = img[0][0]
	q = Queue.Queue()
	v = np.zeros((h,w))
	q.put([h/2,w/2])
	while not q.empty():
		a,b = q.get()
		img3[a][b] = col
		if a>0 and b>0 and v[a-1][b-1]==0 and img[a-1][b-1] != p1:
			q.put([a-1,b-1])
			v[a-1][b-1]=1
		if a>0 and v[a-1][b]==0 and img[a-1][b] != p1:
			q.put([a-1,b])
			v[a-1][b]=1
		if b>0 and v[a][b-1]==0 and img[a][b-1] != p1:
			q.put([a,b-1])
			v[a][b-1]=1
		if a>0 and b<(w-1) and v[a-1][b+1]==0 and img[a-1][b+1] != p1:
			q.put([a-1,b+1])
			v[a-1][b+1]=1
		if b<(w-1) and v[a][b+1]==0 and img[a][b+1] != p1:
			q.put([a,b+1])
			v[a][b+1]=1
		if a<(h-1) and b<(w-1) and v[a+1][b+1]==0 and img[a+1][b+1] != p1:
			q.put([a+1,b+1])
			v[a+1][b+1]=1
		if a<(h-1) and v[a+1][b]==0 and img[a+1][b] != p1:
			q.put([a+1,b])
			v[a+1][b]=1
		if a<(h-1) and b>0 and v[a+1][b-1]==0 and img[a+1][b-1] != p1:
			q.put([a+1,b-1])
			v[a+1][b-1]=1
	
	kernel = np.ones((5,5),np.uint8)
	closing=cv2.morphologyEx(img3,cv2.MORPH_CLOSE,kernel)
	cv2.imwrite("colorUserOut.png",closing)