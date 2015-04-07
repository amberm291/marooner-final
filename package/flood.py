import cv2
import numpy
import sys
import Queue

if __name__ == '__main__':
	img = cv2.imread(sys.argv[1],0)
	img2 = cv2.imread(sys.argv[2],1)
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
		img2[a][b]=[0,0,0]
		if(a>0 and b>0 and v[a-1][b-1]==0 and img[a-1][b-1]==p1):
			q.put([a-1,b-1])
			v[a-1][b-1]=1
		if(a>0 and v[a-1][b]==0 and img[a-1][b]==p1):
			q.put([a-1,b])
			v[a-1][b]=1
		if(b>0 and v[a][b-1]==0 and img[a][b-1]==p1):
			q.put([a,b-1])
			v[a][b-1]=1
		if(a>0 and b<(w-1) and v[a-1][b+1]==0 and img[a-1][b+1]==p1):
			q.put([a-1,b+1])
			v[a-1][b+1]=1
		if(b<(w-1) and v[a][b+1]==0 and img[a][b+1]==p1):
			q.put([a,b+1])
			v[a][b+1]=1
		if(a<(h-1) and b<(w-1) and v[a+1][b+1]==0 and img[a+1][b+1]==p1):
			q.put([a+1,b+1])
			v[a+1][b+1]=1
		if(a<(h-1) and v[a+1][b]==0 and img[a+1][b]==p1):
			q.put([a+1,b])
			v[a+1][b]=1
		if(a<(h-1) and b>0 and v[a+1][b-1]==0 and img[a+1][b-1]==p1):
			q.put([a+1,b-1])
			v[a+1][b-1]=1
	#p1 = [0,0,0]
	for i in range(h):
		for j in range(w):
			if(v[i][j]==0 and img[i][j]==p1):
				img2[i][j][0]=1
	cv2.imwrite("floodOut.png",img2)
