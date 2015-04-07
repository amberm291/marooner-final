import cv2
import numpy as np
import sys
import Queue

if __name__ == '__main__':
	img = cv2.imread(sys.argv[1],1)
	#img2 = cv2.imread(sys.argv[1],1)
	h = img.shape[0]
	w = img.shape[1]
	img2 = np.zeros((h,w,3))
	#for i in range(h):
    #            for j in range(w):
    #                    img2[i][j]=[0,0,0]
	q = Queue.Queue()
	v = np.zeros((h,w))
	q.put([h/2,w/2])
	while not q.empty():
		a,b = q.get()
		img2[a][b] = img[a][b]
		if(a>0 and b>0 and v[a-1][b-1]==0 and (img[a-1][b-1][0]!=0 or img[a-1][b-1][1]!=0 or img[a-1][b-1][2]!=0)):
			q.put([a-1,b-1])
			v[a-1][b-1]=1
		if(a>0 and v[a-1][b]==0 and (img[a-1][b][0]!=0 or img[a-1][b][1]!=0 or img[a-1][b][2]!=0)):
			q.put([a-1,b])
			v[a-1][b]=1
		if(b>0 and v[a][b-1]==0 and (img[a][b-1][0]!=0 or img[a][b-1][1]!=0 or img[a][b-1][2]!=0)):
			q.put([a,b-1])
			v[a][b-1]=1
		if(a>0 and b<(w-1) and v[a-1][b+1]==0 and (img[a-1][b+1][0]!=0 or img[a-1][b+1][1]!=0 or img[a-1][b+1][2]!=0)):
			q.put([a-1,b+1])
			v[a-1][b+1]=1
		if(b<(w-1) and v[a][b+1]==0 and (img[a][b+1][0]!=0 or img[a][b+1][1]!=0 or img[a][b+1][2]!=0)):
			q.put([a,b+1])
			v[a][b+1]=1
		if(a<(h-1) and b<(w-1) and v[a+1][b+1]==0 and (img[a+1][b+1][0]!=0 or img[a+1][b+1][1]!=0 or img[a+1][b+1][2]!=0)):
			q.put([a+1,b+1])
			v[a+1][b+1]=1
		if(a<(h-1) and v[a+1][b]==0 and (img[a+1][b][0]!=0 or img[a+1][b][1]!=0 or img[a+1][b][2]!=0)):
			q.put([a+1,b])
			v[a+1][b]=1
		if(a<(h-1) and b>0 and v[a+1][b-1]==0 and (img[a+1][b-1][0]!=0 or img[a+1][b-1][1]!=0 or img[a+1][b-1][2]!=0)):
			q.put([a+1,b-1])
			v[a+1][b-1]=1
	cv2.imwrite("turdsOut.png",img2)
