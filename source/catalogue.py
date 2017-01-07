#!/usr/bin/python
import cv2
import numpy as np
import Queue

class catPreprocess:
	
	def __init__(self,img):
		self.img = img
		self.leftSegLine = 0
		self.rightSegLine = 0

	def edgeDetect(self,threshold=175):
		edgeImg = cv2.Canny(self.img,10,threshold)
		kernel = np.ones((3,3),np.uint8)
		grayDilated = cv2.dilate(edgeImg,kernel)
		kernel = np.ones((2,2),np.uint8)
		grayErode = cv2.erode(grayDilated,kernel)
		floodOut = self.img
		height,width = grayErode.shape[:2]
		queue = Queue.Queue()
		ref = grayErode[0][0]
		visited = np.zeros((height,width))
		queue.put([0,0])
		queue.put([height-1,width-1])
		queue.put([0, width-1])
		queue.put([height-1,0])
		queue.put([0, width/2])
		queue.put([height-1, width/2])
		while not queue.empty():
			a,b = queue.get()
			floodOut[a][b] = [0,0,0]
			if a>0 and b>0 and visited[a-1][b-1]==0:
				if grayErode[a-1][b-1] == ref:
					queue.put([a-1,b-1])
					visited[a-1][b-1]=1
				else:
					floodOut[a-1][b-1] = [0,0,0]
			if a>0 and visited[a-1][b]==0:
				if grayErode[a-1][b] == ref:
					queue.put([a-1,b])
					visited[a-1][b]=1
				else:
					floodOut[a-1][b] = [0,0,0]
			if b>0 and visited[a][b-1]==0:
				if grayErode[a][b-1] == ref:
					queue.put([a,b-1])
					visited[a][b-1]=1
				else:
					floodOut[a][b-1] = [0,0,0]
			if a>0 and b<(width-1) and visited[a-1][b+1]==0:
				if grayErode[a-1][b+1] == ref:
					queue.put([a-1,b+1])
					visited[a-1][b+1]=1
				else:
					floodOut[a-1][b+1] = [0,0,0]
			if b<(width-1) and visited[a][b+1]==0:
				if grayErode[a][b+1] == ref:
					queue.put([a,b+1])
					visited[a][b+1]=1
				else:
					floodOut[a][b+1] = [0,0,0]
			if a<(height-1) and b<(width-1) and visited[a+1][b+1]==0: 
				if grayErode[a+1][b+1] == ref:
					queue.put([a+1,b+1])
					visited[a+1][b+1]=1
				else:
					floodOut[a+1][b+1] = [0,0,0]
			if a<(height-1) and visited[a+1][b]==0:
				if grayErode[a+1][b] == ref:
					queue.put([a+1,b])
					visited[a+1][b]=1
				else:
					floodOut[a+1][b] = [0,0,0]
			if a<(height-1) and b>0 and visited[a+1][b-1]==0: 
				if grayErode[a+1][b-1] == ref:
					queue.put([a+1,b-1])
					visited[a+1][b-1]=1
				else:
					floodOut[a+1][b-1] = [0,0,0]

		return floodOut

	def discretize(self,n):
		indices = np.arange(0,256)   # List of all colors 
		divider = np.linspace(0,255,n+1)[1] # we get a divider
		quantiz = np.int0(np.linspace(0,255,n)) # we get quantization colors
		color_levels = np.clip(np.int0(indices/divider),0,n-1) # color levels 0,1,2..
		palette = quantiz[color_levels] # Creating the palette
		paletteImg = palette[self.img]  # Applying palette on image
		discreteImg = cv2.convertScaleAbs(paletteImg) # Converting image back to uint8
		return discreteImg

	def flood(self,n):
		discreteOut = self.discretize(n)
		grayDiscrete = cv2.cvtColor(discreteOut, cv2.COLOR_BGR2GRAY)
		floodOut = self.img
		height,width = grayDiscrete.shape[:2]
		queue = Queue.Queue()
		ref = grayDiscrete[0][0]
		visited = np.zeros((height,width))
		queue.put([0,0])
		queue.put([height-1,width-1])
		queue.put([0, width-1])
		queue.put([height-1,0])
		queue.put([0, width/2])
		queue.put([height-1, width/2])
		while not queue.empty():
			a,b = queue.get()
			floodOut[a][b] = [0,0,0]
			if a>0 and b>0 and visited[a-1][b-1]==0 and grayDiscrete[a-1][b-1] == ref:
				queue.put([a-1,b-1])
				visited[a-1][b-1]=1
			if a>0 and visited[a-1][b]==0 and grayDiscrete[a-1][b] == ref:
				queue.put([a-1,b])
				visited[a-1][b]=1
			if b>0 and visited[a][b-1]==0 and grayDiscrete[a][b-1] == ref:
				queue.put([a,b-1])
				visited[a][b-1]=1
			if a>0 and b<(width-1) and visited[a-1][b+1]==0 and grayDiscrete[a-1][b+1] == ref:
				queue.put([a-1,b+1])
				visited[a-1][b+1]=1
			if b<(width-1) and visited[a][b+1]==0 and grayDiscrete[a][b+1] == ref:
				queue.put([a,b+1])
				visited[a][b+1]=1
			if a<(height-1) and b<(width-1) and visited[a+1][b+1]==0 and grayDiscrete[a+1][b+1] == ref:
				queue.put([a+1,b+1])
				visited[a+1][b+1]=1
			if a<(height-1) and visited[a+1][b]==0 and grayDiscrete[a+1][b] == ref:
				queue.put([a+1,b])
				visited[a+1][b]=1
			if a<(height-1) and b>0 and visited[a+1][b-1]==0 and grayDiscrete[a+1][b-1] == ref:
				queue.put([a+1,b-1])
				visited[a+1][b-1]=1

		grayDisrete = cv2.cvtColor(floodOut, cv2.COLOR_BGR2GRAY)
		visited = np.zeros((height,width))
		queue.put([0,0,0])
		queue.put([height-1,width-1,0])
		queue.put([0, width-1,0])
		queue.put([height-1,0,0])
		queue.put([0, width/2,0])
		queue.put([height-1, width/2,0])
		while not queue.empty():
			a,b,c = queue.get()
			floodOut[a][b] = [0,0,0]
			if c == 3:
				continue
			for i in range(-1,2):
				for j in range(-1,2):
					if i==0 and j == 0:
						continue
					if (a+i) >= 0 and (a+i) < height and (b+j) >= 0 and (b+j) < width and visited[a+i][b+j] == 0 and (floodOut[a+i][b+j] == floodOut[0][0]).all():
						queue.put([a+i,b+j,0])
						visited[a+i][b+j]=1
					elif (a+i) >= 0 and (a+i) < height and (b+j) >= 0 and (b+j) < width and visited[a+i][b+j] == 0:
						queue.put([a+i,b+j,c+1])
						visited[a+i][b+j]=1
		return floodOut

	def cropImg(self,img):
		img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		height = img.shape[0]
		width = img.shape[1]

		check = 0

		Left = 0
		Right = 0
		Top = 0
		Bottom = 0

		for j in xrange(0, width):
			for i in xrange(0, height):
				if(img[i][j] != img[0][0]):
					Left = j
					check = 1
					break
			if(check == 1):
				break

		check = 0

		for j in xrange(width-1, -1, -1):
			for i in xrange(0, height):
				if(img[i][j] != img[0][0]):
					Right = j
					check = 1
					break
			if(check == 1):
				break

		check = 0

		for i in xrange(height-1, -1, -1):
			for j in xrange(0, width):
				if(img[i][j] != img[0][0]):
					Bottom = i
					check = 1
					break
			if(check == 1):
				break
		check = 0

		for i in xrange(0, height):
			for j in xrange(0, width):
				if(img[i][j] != img[0][0]):
					Top = i
					check = 1
					break
			if(check == 1):
				break

		crop_img = self.img[Top:Bottom, Left:Right]

		return crop_img

	def segImage(self,floodOut):
		grayCatImg = cv2.cvtColor(floodOut,cv2.COLOR_BGR2GRAY)
		i = grayCatImg.shape[0]/2
		for j in xrange(0, grayCatImg.shape[1]):
			if grayCatImg[i][j] != grayCatImg[0][0]:
				self.leftSegLine = j
				break

		for j in xrange(grayCatImg.shape[1]-1,-1,-1):
			if grayCatImg[i][j] != grayCatImg[0][0] :
				self.rightSegLine = j
				break 

		LPrev = self.leftSegLine
		RPrev = self.rightSegLine

		check = 0

		self.leftSegLine = 0
		self.rightSegLine = 0

		prevI = 0
		start = -1
		for i in xrange(grayCatImg.shape[0]/2, -1, -1):
			cnt=start
			for j in xrange(grayCatImg.shape[1]/2, -1, -1):
				if (cnt == 1) and (grayCatImg[i][j] != 0):
					cnt = 2
					start = 0
					prevI = i
					break
				if (cnt == start) and (grayCatImg[i][j] == 0):
					cnt = 1
			if (cnt == 1) and (start != -1):
				break


		for j in xrange(grayCatImg.shape[1]/2, -1, -1):
			if grayCatImg[prevI+1][j] == 0:
				prevJ1 = j
				break

		for j in xrange(grayCatImg.shape[1]/2, -1, -1):
			if grayCatImg[prevI][j] == 0 :
				prevJ2 = j
				break

		self.leftSegLine = min(prevJ1, prevJ2)

		prevI = 0
		start = -1
		for i in xrange(grayCatImg.shape[0]/2, -1, -1):
			cnt=start
			for j in xrange(grayCatImg.shape[1]/2, grayCatImg.shape[1]):
				if (cnt == 1) and (grayCatImg[i][j] != 0):
					cnt = 2
					start = 0
					prevI = i
					break
				if (cnt == start) and (grayCatImg[i][j] == 0):
					cnt = 1
			if(cnt == 1 and start != -1):
				break


		for j in xrange(grayCatImg.shape[1]/2, grayCatImg.shape[1]):
			if grayCatImg[prevI+1][j] == 0 :
				prevJ1 = j
				break

		for j in xrange(grayCatImg.shape[1]/2, grayCatImg.shape[1]):
			if grayCatImg[prevI][j] == 0:
				prevJ2 = j
				break

		self.rightSegLine = min(prevJ1, prevJ2)


		if(abs(grayCatImg.shape[1]/2-self.leftSegLine)<abs(LPrev-self.leftSegLine)):
			self.leftSegLine = LPrev
		if(abs(grayCatImg.shape[1]/2-self.rightSegLine)<abs(RPrev-self.rightSegLine)):
			self.rightSegLine = RPrev
		if(abs(LPrev/2-self.leftSegLine)<abs(LPrev-self.leftSegLine)):
			self.leftSegLine = LPrev
		if(abs(RPrev + (grayCatImg.shape[1]-RPrev)/2 - self.rightSegLine)<abs(RPrev-self.rightSegLine)):
			self.rightSegLine = RPrev

	def getSegLines(self):
		return self.leftSegLine,self.rightSegLine

	def armSegment(self,img,leftOrRight):
		if leftOrRight == 'left':
			segImg = img.copy()
			segImg[:,self.leftSegLine+1:] = 0
			return self.armRemTurds(segImg,leftOrRight)
		else:
			segImg = img.copy()
			segImg[:,0:self.rightSegLine-1] = 0
			return self.armRemTurds(segImg,leftOrRight)

	def armRemTurds(self,img,leftOrRight):
		grayImg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		height = img.shape[0]
		width = img.shape[1]
		queue = Queue.Queue()
		if leftOrRight == 'left':
			for i in xrange(img.shape[0]):
				if grayImg[i][self.leftSegLine-1] != 0:
					initPt = i
					break
			queue.put([initPt,self.leftSegLine-1])

		else:
			for i in xrange(img.shape[0]):
				if grayImg[i][self.rightSegLine+1] != 0:
					initPt = i
					break
			queue.put([initPt,self.rightSegLine+1])

		turdsOut = np.zeros((height,width,3))
		visited = np.zeros((height,width))

		while not queue.empty():
			a,b = queue.get()
			turdsOut[a][b] = img[a][b]
			if a>0 and b>0 and visited[a-1][b-1]==0 and grayImg[a-1][b-1] != 0:
				queue.put([a-1,b-1])
				visited[a-1][b-1]=1
			if a>0 and visited[a-1][b]==0 and grayImg[a-1][b] != 0:
				queue.put([a-1,b])
				visited[a-1][b]=1
			if b>0 and visited[a][b-1]==0 and grayImg[a][b-1] != 0:
				queue.put([a,b-1])
				visited[a][b-1]=1
			if a>0 and b<(width-1) and visited[a-1][b+1]==0 and grayImg[a-1][b+1] != 0:
				queue.put([a-1,b+1])
				visited[a-1][b+1]=1
			if b<(width-1) and visited[a][b+1]==0 and grayImg[a][b+1] != 0:
				queue.put([a,b+1])
				visited[a][b+1]=1
			if a<(height-1) and b<(width-1) and visited[a+1][b+1]==0 and grayImg[a+1][b+1] != 0:
				queue.put([a+1,b+1])
				visited[a+1][b+1]=1
			if a<(height-1) and visited[a+1][b]==0 and grayImg[a+1][b] != 0:
				queue.put([a+1,b])
				visited[a+1][b]=1
			if a<(height-1) and b>0 and visited[a+1][b-1]==0 and grayImg[a+1][b-1] != 0:
				queue.put([a+1,b-1])
				visited[a+1][b-1]=1

		#cv2.imwrite("debug/turdsOut.jpg",turdsOut)
		return np.uint8(turdsOut)