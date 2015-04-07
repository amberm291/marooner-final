import cv2
import numpy as np
import sys
import Queue

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[2],1)
img3 = img

LU = input()
RU = input()
LP = input()
RP = input()

for i in range(img.shape[0]):
	if(img[i][LU][0]!=img[0][0][0] or img[i][LU][1]!=img[0][0][1] or img[i][LU][2]!=img[0][0][2]):
		p1=i
		break

for i in range(img2.shape[0]):
	if(img2[i][LP][0]!=img2[0][0][0] or img2[i][LP][1]!=img2[0][0][1] or img2[i][LP][2]!=img2[0][0][2]):
		p2=i
		break

'''imgDeb = img
for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		if(i == p1):
			imgDeb[i][j][0]=imgDeb[i][j][1]=imgDeb[i][j][2]=0

img2Deb = img2
for i in range(img2.shape[0]):
	for j in range(img2.shape[1]):
		if(i == p2):
			img2Deb[i][j][0]=img2Deb[i][j][1]=img2Deb[i][j][2]=0
cv2.imwrite("imgDeb.png", imgDeb)
cv2.imwrite("img2Deb.png", img2Deb)

startpix = []
endpix = []
startpix2 = []
endpix2 = []

mid = int(img.shape[1]/2)
midStart = mid-5
midEnd = mid+5
minH = img.shape[0]
mid1 = 0
mid2 = 0
for i in range(0, img.shape[0]):
	for j in range(midStart, midEnd+1):
		if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
			if(minH>i):
				minH=i
				mid1=j
			break

mid = int(img2.shape[1]/2)
minH = img2.shape[0]
midStart = mid-5
midEnd = mid+5
for i in range(0, img2.shape[0]):
	for j in range(midStart, midEnd+1):
		if(img2[i][j][0] != img2[0][0][0] or img2[i][j][1] != img2[0][0][1] or img2[i][j][2] != img2[0][0][2]):
			if(minH>i):
				minH=i
				mid2=j
			break
'''
mid1 = int((LU+RU)/2)
mid2 = int((LP+RP)/2)
print mid1
print mid2
'''h,w = img2.shape[:2]
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
for i in range(h):
	for j in range(w):
		if(v[i][j]==0 and img2[i][j][0]==0 and img2[i][j][1]==0 and img2[i][j][2]==0):
			img2[i][j][2]=1'''
for i in range(0,img.shape[0]):
	if(i+p2-p1 >= img2.shape[0]):
		break
	for j in range(mid1, img.shape[1]):
		if(mid2+j-mid1 < img2.shape[1]):
			if((img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2])and(img2[i+p2-p1][mid2+j-mid1][0]!=img2[0][0][0] or img2[i+p2-p1][mid2+j-mid1][1]!=img2[0][0][1] or img2[i+p2-p1][mid2+j-mid1][2]!=img2[0][0][2])):
				img3[i][j] = img2[i+p2-p1][mid2+j-mid1]

for i in range(0, img.shape[0]):
	if(i+p2-p1 >= img2.shape[0]):
		break
	for j in range(mid1-1, -1, -1):
		if(mid2+j-mid1>=0):
			if((img[i][j][0]!=img[0][0][0] or img[i][j][1]!=img[0][0][1] or img[i][j][2]!=img[0][0][2])and(img2[i+p2-p1][mid2+j-mid1][0]!=img2[0][0][0] or img2[i+p2-p1][mid2+j-mid1][1]!=img2[0][0][1] or img2[i+p2-p1][mid2+j-mid1][2]!=img2[0][0][2])):
				img3[i][j] = img2[i+p2-p1][mid2+j-mid1]
print "P1 P2 : "
print p1
print p2

cv2.imwrite("resultfitver5.png", img3)