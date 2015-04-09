#!/usr/bin/python

import cv2
import numpy as np
from scipy import ndimage
import Queue

class grabcut:
	BLUE = [255,0,0]        # rectangle color
	RED = [0,0,255]         # PR BG
	GREEN = [0,255,0]       # PR FG
	BLACK = [0,0,0]         # sure BG
	WHITE = [255,255,255]   # sure FG

	DRAW_BG = {'color' : BLACK, 'val' : 0}
	DRAW_FG = {'color' : WHITE, 'val' : 1}
	DRAW_PR_FG = {'color' : GREEN, 'val' : 3}
	DRAW_PR_BG = {'color' : RED, 'val' : 2}

	
	def __init__(self, userImage):
		self.img = userImage
		self.mask = np.zeros(self.img.shape[:2],dtype = np.uint8)
		self.img2 = self.img.copy()
		# setting up flags
		self.rect = (0,0,1,1)
		self.drawing = False         # flag for drawing curves
		self.rectangle = False       # flag for drawing rect
		self.rect_over = False       # flag to check if rect drawn
		self.rect_or_mask = 100      # flag for selecting rect or mask mode
		self.value = self.DRAW_FG         # drawing initialized to FG
		self.thickness = 3           # brush thickness
		

	def onmouse(self,event,x,y,flags,param):
		global ix,iy
				
		if event == cv2.EVENT_RBUTTONDOWN:
		    self.rectangle = True
		    ix,iy = x,y

		elif event == cv2.EVENT_MOUSEMOVE:
		    if self.rectangle == True:
		    	self.img = self.img2.copy()
		        cv2.rectangle(self.img,(ix,iy),(x,y),self.BLUE,2)
		        self.rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))
		        self.rect_or_mask = 0

		elif event == cv2.EVENT_RBUTTONUP:
		    self.rectangle = False
		    self.rect_over = True
		    cv2.rectangle(self.img,(ix,iy),(x,y),self.BLUE,2)
		    self.rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))
		    self.rect_or_mask = 0
		    print " Now press the key 'n' a few times until no further change \n"

		# draw touchup curves

		if event == cv2.EVENT_LBUTTONDOWN:
		    if self.rect_over == False:
		        print "first draw rectangle \n"
		    else:
		        self.drawing = True
		        cv2.circle(self.img,(x,y),self.thickness,self.value['color'],-1)
		        cv2.circle(self.mask,(x,y),self.thickness,self.value['val'],-1)

		elif event == cv2.EVENT_MOUSEMOVE:
		    if self.drawing == True:
		        cv2.circle(self.img,(x,y),self.thickness,self.value['color'],-1)
		        cv2.circle(self.mask,(x,y),self.thickness,self.value['val'],-1)

		elif event == cv2.EVENT_LBUTTONUP:
		    if self.drawing == True:
		        self.drawing = False
		        cv2.circle(self.img,(x,y),self.thickness,self.value['color'],-1)
		        cv2.circle(self.mask,(x,y),self.thickness,self.value['val'],-1)

	def grabcut(self):
		#self.img = self.userImage
		#img2 = img.copy()                               # a copy of original image
		#mask = self.mask 								# mask initialized to PR_BG
		output = np.zeros(self.img.shape,np.uint8)           # output image to be shown

		# input and output windows
		cv2.namedWindow('output')
		cv2.namedWindow('input')
		cv2.setMouseCallback('input',self.onmouse)
		cv2.moveWindow('input',self.img.shape[1]+10,90)

		print " Instructions: \n"
		print " Draw a rectangle around the object using right mouse button \n"

		while(1):

		    cv2.imshow('output',output)
		    cv2.imshow('input',self.img)
		    k = 0xFF & cv2.waitKey(1)

		    # key bindings
		    if k == 27:         # esc to exit
		        break
		    elif k == ord('0'): # BG self.drawing
		        print " mark background regions with left mouse button \n"
		        self.value = self.DRAW_BG
		    elif k == ord('1'): # FG drawing
		        print " mark foreground regions with left mouse button \n"
		        self.value = self.DRAW_FG
		    elif k == ord('2'): # PR_BG drawing
		        self.value = self.DRAW_PR_BG
		    elif k == ord('3'): # PR_FG drawing
		        self.value = self.DRAW_PR_FG
		    elif k == ord('s'): # save image
		        bar = np.zeros((self.img.shape[0],5,3),np.uint8)
		        res = np.hstack((self.img2,bar,self.img,bar,output))
		        res2 = np.hstack((output))
		        cv2.destroyAllWindows()
		        return output
		        #cv2.imwrite('grabcut_output.jpg',res)
		        print " Result saved as image \n"
		    elif k == ord('r'): # reset everything
		        print "resetting \n"
		        self.rect = (0,0,1,1)
		        self.drawing = False
		        self.rectangle = False
		        self.rect_or_mask = 100
		        self.rect_over = False
		        self.value = self.DRAW_FG
		        self.img = self.img2.copy()
		        self.mask = np.zeros(self.img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG
		        output = np.zeros(self.img.shape,np.uint8)           # output image to be shown
		    elif k == ord('n'): # segment the image
		        print """ For finer touchups, mark foreground and background after pressing keys 0-3
		        and again press 'n' \n"""
		        if (self.rect_or_mask == 0):         # grabcut with rect
		            bgdmodel = np.zeros((1,65),np.float64)
		            fgdmodel = np.zeros((1,65),np.float64)
		            cv2.grabCut(self.img2,self.mask,self.rect,bgdmodel,fgdmodel,10,cv2.GC_INIT_WITH_RECT)
		            self.rect_or_mask = 1
		        elif self.rect_or_mask == 1:         # grabcut with mask
		            bgdmodel = np.zeros((1,65),np.float64)
		            fgdmodel = np.zeros((1,65),np.float64)
		            cv2.grabCut(self.img2,self.mask,self.rect,bgdmodel,fgdmodel,10,cv2.GC_INIT_WITH_MASK)

		    mask2 = np.where((self.mask==1) + (self.mask==3),255,0).astype('uint8')
		    output = cv2.bitwise_and(self.img2,self.img2,mask=mask2)

		cv2.destroyAllWindows()

class userPreprocess:
	def __init__(self,userImage):
		self.img = userImage
		self.leftSegLine = 0
		self.rightSegLine = 0
		self.Top = 0
		self.Bottom = 0
		self.Left = 0
		self.Right = 0
	
	def cropImg(self):
		labels, numLabels = ndimage.label(self.img)
		fragments = ndimage.find_objects(labels)
		self.Top = fragments[0][0].start
		self.Bottom = fragments[0][0].stop
		self.Left = fragments[0][1].start
		self.Right = fragments[0][1].stop
		Area = 0
		for slices in fragments:
			segArea = (slices[0].stop - slices[0].start)*(slices[1].stop - slices[1].start)
			if segArea >= Area:
				Area = segArea
				self.Top = slices[0].start
				self.Bottom = slices[0].stop
				self.Left = slices[1].start
				self.Right = slices[1].stop
		self.img = self.img[self.Top:self.Bottom, self.Left:self.Right]

	def returnUserBox(self):
		return [self.Top,self.Bottom,self.Left,self.Right]

	def removeTurds(self):
		grayImg = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
		height = grayImg.shape[0]
		width = grayImg.shape[1]
		for i in xrange(height):
			if grayImg[i][width/2]:
				initPt = i
		#initPt += 1
		turdsOut = np.zeros((height,width,3))
		queue = Queue.Queue()
		visited = np.zeros((height,width))
		queue.put([initPt,width/2])
		while not queue.empty():
			a,b = queue.get()
			turdsOut[a][b] = self.img[a][b]
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
	
	def segImage(self,cropOut):
		grayUserImg = cv2.cvtColor(cropOut,cv2.COLOR_BGR2GRAY)
		i = grayUserImg.shape[0]/2
		for j in xrange(0, grayUserImg.shape[1]):
			if grayUserImg[i][j] != grayUserImg[0][0]:
				self.leftSegLine = j
				break

		for j in xrange(grayUserImg.shape[1]-1,-1,-1):
			if grayUserImg[i][j] != grayUserImg[0][0] :
				self.rightSegLine = j
				break 

		LPrev = self.leftSegLine
		RPrev = self.rightSegLine

		check = 0

		self.leftSegLine = 0
		self.rightSegLine = 0

		prevI = 0
		start = -1
		for i in xrange(grayUserImg.shape[0]/2, -1, -1):
			cnt=start
			for j in xrange(grayUserImg.shape[1]/2, -1, -1):
				if (cnt == 1) and (grayUserImg[i][j] != 0):
					cnt = 2
					start = 0
					prevI = i
					break
				if (cnt == start) and (grayUserImg[i][j] == 0):
					cnt = 1
			if (cnt == 1) and (start != -1):
				break


		for j in xrange(grayUserImg.shape[1]/2, -1, -1):
			if grayUserImg[prevI+1][j] == 0:
				prevJ1 = j
				break

		for j in xrange(grayUserImg.shape[1]/2, -1, -1):
			if grayUserImg[prevI][j] == 0 :
				prevJ2 = j
				break

		self.leftSegLine = min(prevJ1, prevJ2)

		prevI = 0
		start = -1
		for i in xrange(grayUserImg.shape[0]/2, -1, -1):
			cnt=start
			for j in xrange(grayUserImg.shape[1]/2, grayUserImg.shape[1]):
				if (cnt == 1) and (grayUserImg[i][j] != 0):
					cnt = 2
					start = 0
					prevI = i
					break
				if (cnt == start) and (grayUserImg[i][j] == 0):
					cnt = 1
			if cnt == 1 and start != -1:
				break


		for j in xrange(grayUserImg.shape[1]/2, grayUserImg.shape[1]):
			if grayUserImg[prevI+1][j] == 0 :
				prevJ1 = j
				break

		for j in xrange(grayUserImg.shape[1]/2, grayUserImg.shape[1]):
			if grayUserImg[prevI][j] == 0:
				prevJ2 = j
				break

		self.rightSegLine = min(prevJ1, prevJ2)


		if(abs(grayUserImg.shape[1]/2-self.leftSegLine)<abs(LPrev-self.leftSegLine)):
			self.leftSegLine = LPrev
		if(abs(grayUserImg.shape[1]/2-self.rightSegLine)<abs(RPrev-self.rightSegLine)):
			self.rightSegLine = RPrev
		if(abs(LPrev/2-self.leftSegLine)<abs(LPrev-self.leftSegLine)):
			self.leftSegLine = LPrev
		if(abs(RPrev + (grayUserImg.shape[1]-RPrev)/2 - self.rightSegLine)<abs(RPrev-self.rightSegLine)):
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

