#!/usr/bin/python

import cv2
import numpy as np
import Queue
import math
from scipy import ndimage
from user import userPreprocess
from catalogue import catPreprocess

class userFit(userPreprocess,catPreprocess):

	def __init__(self,userImg,catImg):
		self.userImg = userImg
		self.catImg = catImg
		self.catImgSleeve = None
		self.ratio = 1
		self.leftUserLine = 0
		self.rightUserLine = 0
		self.leftCatLine = 0
		self.rightCatLine = 0
		self.userMid = 0
		self.catMid = 0
		self.userShLine = 0
		self.catShLine = 0
		self.Top = 0
		self.Bottom = 0
		self.Left = 0
		self.Right = 0
		self.leftArmUser = None
		self.rightArmUser = None
		self.leftArmCat = None
		self.rightArmCat = None

	def colorUser(self):
		grayUserImg = cv2.cvtColor(self.userImg,cv2.COLOR_BGR2GRAY)
		color = self.catImg[self.catImg.shape[0]/2][self.catImg.shape[1]/2]
		height,width = grayUserImg.shape[:2]
		ref = grayUserImg[0][0]
		queue = Queue.Queue()
		visited = np.zeros((height,width))
		queue.put([0,0])
		queue.put([height-1,width-1])
		queue.put([0, width-1])
		queue.put([height-1,0])
		queue.put([0, width/2])
		queue.put([height-1, width/2])
		
		while not queue.empty():
			a,b = queue.get()
			if a>0 and b>0 and visited[a-1][b-1]==0 and grayUserImg[a-1][b-1] == ref:
				queue.put([a-1,b-1])
				visited[a-1][b-1]=1
			if a>0 and visited[a-1][b]==0 and grayUserImg[a-1][b] == ref:
				queue.put([a-1,b])
				visited[a-1][b]=1
			if b>0 and visited[a][b-1]==0 and grayUserImg[a][b-1] == ref:
				queue.put([a,b-1])
				visited[a][b-1]=1
			if a>0 and b<(width-1) and visited[a-1][b+1]==0 and grayUserImg[a-1][b+1] == ref:
				queue.put([a-1,b+1])
				visited[a-1][b+1]=1
			if b<(width-1) and visited[a][b+1]==0 and grayUserImg[a][b+1] == ref:
				queue.put([a,b+1])
				visited[a][b+1]=1
			if a<(height-1) and b<(width-1) and visited[a+1][b+1]==0 and grayUserImg[a+1][b+1] == ref:
				queue.put([a+1,b+1])
				visited[a+1][b+1]=1
			if a<(height-1) and visited[a+1][b]==0 and grayUserImg[a+1][b] == ref:
				queue.put([a+1,b])
				visited[a+1][b]=1
			if a<(height-1) and b>0 and visited[a+1][b-1]==0 and grayUserImg[a+1][b-1] == ref:
				queue.put([a+1,b-1])
				visited[a+1][b-1]=1

		for i in xrange(grayUserImg.shape[0]):
			for j in xrange(grayUserImg.shape[1]):
				if(visited[i][j]==0):
					self.userImg[i][j][0]=color[0]
					self.userImg[i][j][1]=color[1]
					self.userImg[i][j][2]=color[2]

		kernel = np.ones((5,5),np.uint8)
		colorUserOut = cv2.morphologyEx(self.userImg,cv2.MORPH_CLOSE,kernel)
		return colorUserOut

	def resizeCat(self):
		oldLen = self.catImg.shape[1]
		self.catImg = cv2.resize(self.catImg,(int(self.userImg.shape[1]),int(self.userImg.shape[0])))
		self.catImgSleeve = self.catImg
		
		grayUserImg = cv2.cvtColor(self.userImg,cv2.COLOR_BGR2GRAY)
		grayCatImg = cv2.cvtColor(self.catImg,cv2.COLOR_BGR2GRAY)
		
		pixCountUser = 0
		pixCountCat = 0

		for j in xrange(grayUserImg.shape[1]):
			if grayUserImg[grayUserImg.shape[0]-100][j] != 0:
				pixCountUser += 1

		for j in xrange(grayCatImg.shape[1]):
			if grayCatImg[grayCatImg.shape[0]-100][j] != 0:
				pixCountCat += 1
	
		self.ratio += float(pixCountCat-pixCountUser)/float(grayUserImg.shape[1])
		#print self.ratio
		self.catImg = cv2.resize(self.catImg, (int(self.ratio*self.userImg.shape[1]), int(self.ratio*self.userImg.shape[0])),interpolation=cv2.INTER_NEAREST)
		self.leftArmCat = cv2.resize(self.leftArmCat, (int(self.ratio*self.userImg.shape[1]), int(self.ratio*self.userImg.shape[0])),interpolation=cv2.INTER_NEAREST)
		self.rightArmCat = cv2.resize(self.rightArmCat, (int(self.ratio*self.userImg.shape[1]), int(self.ratio*self.userImg.shape[0])),interpolation=cv2.INTER_NEAREST)

		self.leftCatLine *= float(self.catImg.shape[1])/float(oldLen)
		self.leftCatLine = int(self.leftCatLine)
		self.rightCatLine *= float(self.catImg.shape[1])/float(oldLen)
		self.rightCatLine = int(self.rightCatLine)
		#print self.leftCatLine,self.rightCatLine,self.leftUserLine,self.rightUserLine
		#cv2.imwrite('debug/resizedCatImg.jpg',self.catImg)
		#return self.catImg

	def setSegLines(self,leftCat,rightCat,leftUser,rightUser):
		self.leftCatLine = leftCat
		self.rightCatLine = rightCat
		self.leftUserLine = leftUser
		self.rightUserLine = rightUser

	def setUserBox(self,l):	#top,bottom,left,right
		self.Top = l[0]
		self.Bottom = l[1]
		self.Left = l[2]
		self.Right = l[3]

	def bodyFit(self, colorUserImg):
		#Previously fitver5.py
		grayUserImg = cv2.cvtColor(self.userImg,cv2.COLOR_BGR2GRAY)
		bodyFitOut  = self.userImg.copy()
		#self.segImage(colorUserImg)
		#grayCatImg = cv2.cvtColor(self.catImg,cv2.COLOR_BGR2GRAY)

		for i in xrange(grayUserImg.shape[0]):
			if grayUserImg[i][self.leftUserLine] != grayUserImg[0][0]:
				self.userShLine = i
				break

		for i in xrange(self.catImg.shape[0]):
			if (self.catImg[i][self.leftCatLine] != self.catImg[0][0]).any():
				self.catShLine = i
				break

		self.userMid = int((self.leftUserLine + self.rightUserLine)/2)
		self.catMid = int((self.leftCatLine + self.rightCatLine)/2)

		#print self.userMid, self.catMid, self.userShLine, self.catShLine
		for i in xrange(0,grayUserImg.shape[0]):
			if i + self.catShLine - self.userShLine >= self.catImg.shape[0]:
				break
			for j in xrange(self.userMid, grayUserImg.shape[1]):
				if self.catMid + j - self.userMid < self.catImg.shape[1]:
					if grayUserImg[i][j] != grayUserImg[0][0] and (self.catImg[i + self.catShLine - self.userShLine][self.catMid + j - self.userMid] != self.catImg[0][0]).any():
						bodyFitOut[i][j] = self.catImg[i + self.catShLine - self.userShLine][self.catMid + j - self.userMid]
		
		for i in xrange(0,grayUserImg.shape[0]):
			if i + self.catShLine - self.userShLine >= self.catImg.shape[0]:
				break
			for j in xrange(self.userMid, -1, -1):
				if self.catMid + j - self.userMid >= 0:
					if grayUserImg[i][j] != grayUserImg[0][0] and (self.catImg[i + self.catShLine - self.userShLine][self.catMid + j - self.userMid] != self.catImg[0][0]).any():
						bodyFitOut[i][j] = self.catImg[i + self.catShLine - self.userShLine][self.catMid + j - self.userMid]
		
		return bodyFitOut

	'''
	def sleeveFit(self,bodyFitOut):
		finalFit = bodyFitOut
		startUser = []
		endUser = []
		startCat = []
		endCat = []
		for j in xrange(0, bodyFitOut.shape[1]):
			for i in xrange(0, bodyFitOut.shape[0]):
				if bodyFitOut[i][j][0] != bodyFitOut[0][0][0] or bodyFitOut[i][j][1] != bodyFitOut[0][0][1] or bodyFitOut[i][j][2] != bodyFitOut[0][0][2]:
					startUser.append(i)
					break

		for j in xrange(0, bodyFitOut.shape[1]):
			for i in xrange(startUser[j], bodyFitOut.shape[0]):
				if bodyFitOut[i][j][0] == bodyFitOut[0][0][0] and bodyFitOut[i][j][1] == bodyFitOut[0][0][1] and bodyFitOut[i][j][2] == bodyFitOut[0][0][2]:
					endUser.append(i-1)
					break
				if i == bodyFitOut.shape[0]-1:
					endUser.append(i)

		for j in xrange(0, self.catImgSleeve.shape[1]):
			for i in xrange(0, self.catImgSleeve.shape[0]):
				if self.catImgSleeve[i][j][0] != self.catImgSleeve[0][0][0] or self.catImgSleeve[i][j][1] != self.catImgSleeve[0][0][1] or self.catImgSleeve[i][j][2] != self.catImgSleeve[0][0][2]:
					startCat.append(i)
					break

		for j in xrange(0, self.catImgSleeve.shape[1]):
			for i in xrange(startCat[j], self.catImgSleeve.shape[0]):
				if self.catImgSleeve[i][j][0] == self.catImgSleeve[0][0][0] and self.catImgSleeve[i][j][1] == self.catImgSleeve[0][0][1] and self.catImgSleeve[i][j][2] == self.catImgSleeve[0][0][2]:
					endCat.append(i-1)
					break
				if i == self.catImgSleeve.shape[0]-1:
					endCat.append(i)

		for j in xrange(0, bodyFitOut.shape[1]):
			if(j <= self.leftUserLine or j >= self.rightUserLine):
				for i in xrange((startUser[j]+endUser[j])/2,startUser[j]-1,-1):
					if((startCat[j]+endCat[j])/2+i-(startUser[j]+endUser[j])/2 >= startCat[j]):
						finalFit[i][j] = self.catImgSleeve[(startCat[j]+endCat[j])/2+i-(startUser[j]+endUser[j])/2][j]
				for i in xrange((startUser[j]+endUser[j])/2,endUser[j]+1):
					if((startCat[j]+endCat[j])/2+i-(startUser[j]+endUser[j])/2 < endCat[j]):
						finalFit[i][j] = self.catImgSleeve[(startCat[j]+endCat[j])/2+i-(startUser[j]+endUser[j])/2][j]

		return finalFit
	'''
	def fittingOntoUser(self,finalFit,userImg):
		for i in xrange(self.Top,self.Bottom):
			for j in xrange(self.Left,self.Right):
				if (finalFit[i-self.Top][j-self.Left]==[0,0,0]).all():
					pass
				else:
					userImg[i][j] = finalFit[i-self.Top][j-self.Left]
		return userImg

	def setUserArm(self,left,right):
		self.leftArmUser = left
		self.rightArmUser = right

	def setCatArm(self,left,right):
		self.leftArmCat = left
		self.rightArmCat = right

	def getBox(self,img):
		grayImg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		leftX = leftY = upX = upY = rightX = rightY = downX = downY = 0.0

		for i in xrange(grayImg.shape[0]):
			for j in xrange(grayImg.shape[1]):
				if upX == 0 and upY == 0:
					if grayImg[i][j] != grayImg[0][0]:
						upX = j
						upY = i
			if upX != 0 or upY != 0:
				break

		for i in xrange(grayImg.shape[0]-1, -1, -1):
			for j in xrange(grayImg.shape[1]):
				if downX == 0 and downY == 0:
					if grayImg[i][j] != grayImg[0][0]:
						downX = j
						downY = i
			if downX != 0 or downY != 0:
				break

		for j in xrange(grayImg.shape[1]):
			for i in xrange(grayImg.shape[0]):
				if leftX == 0 and leftY == 0:
					if grayImg[i][j] != grayImg[0][0]:
						leftX = j
						leftY = i
			if leftX != 0 or leftY != 0:
				break

		for j in xrange(grayImg.shape[1]-1, -1, -1):
			for i in xrange(grayImg.shape[0]):
				if rightX == 0 and rightY == 0:
					if grayImg[i][j] != grayImg[0][0]:
						rightX = j
						rightY = i
			if rightX != 0 or rightY != 0:
				break

		return [leftX, leftY,rightX, rightY,upX, upY,downX, downY]

	def rotateImage(self,img,theta,mid1,mid2):
		M = cv2.getRotationMatrix2D((mid1, mid2),theta,1)
		dst = cv2.warpAffine(img,M,(img.shape[1],img.shape[0]), flags= cv2.INTER_NEAREST)
		extra = 200
		cropImg = dst[extra:dst.shape[0]-extra, extra:dst.shape[1]-extra]
		#cv2.imwrite("finalrotate"+s + ".jpg", cropimg)
		return cropImg

	def rotateNSave(self,img,leftOrRight):
		lx, ly, rx, ry, ux, uy, dx, dy = self.getBox(img)
		
		check_inf = 0
		if leftOrRight == 'left':
			if ux == lx:
				check_inf = 1
			else:
				slope = (1.0*uy-ly)/(ux-lx)
		else:
			if ux == rx:
				check_inf = 1
			else:
				slope = (1.0*uy-ry)/(ux-rx)

		midX = ux
		midY = uy

		if check_inf == 0:
			theta = math.degrees(math.atan(slope))
		else:
			theta = 90
			if leftOrRight == 'right':
				theta = -90

		M = cv2.getRotationMatrix2D((midX, midY),theta,1)
		dst = cv2.warpAffine(img,M,(img.shape[1],img.shape[0]),flags= cv2.INTER_NEAREST)
		return dst,ux,uy,theta

	def leftFit(self,userImg,catImg):
		grayUser = cv2.cvtColor(userImg,cv2.COLOR_BGR2GRAY)
		grayCat = cv2.cvtColor(catImg,cv2.COLOR_BGR2GRAY)

		check = 0
		for i in xrange(grayUser.shape[0]):
			for j in xrange(grayUser.shape[1]):
				if grayUser[i][j] != grayUser[0][0]:
					self.userShLine = i
					check = 1
					break
			if check != 0:
				break
		
		check = 0
		for i in xrange(grayCat.shape[0]):
			for j in xrange(grayCat.shape[1]):
				if grayCat[i][j] != grayCat[0][0]:
					self.catShLine = i
					check = 1
					break
			if check != 0:
				break
		
		startUser = [0]*grayUser.shape[0]
		startCat= [0]*grayCat.shape[0]
		endUser = [0]*grayUser.shape[0]
		endCat = [0]*grayCat.shape[0]

		for i in xrange(self.userShLine,grayUser.shape[0]):
			check = 0
			prev = 0
			for j in xrange(grayUser.shape[1]):
				if check == 0 and grayUser[i][j] != grayUser[0][0]:
					startUser[i] = j
					check = 1
				elif check == 1 and grayUser[i][j] == grayUser[0][0]:
					if prev != (j-1):
						endUser[i] = j
					prev = j

		for i in xrange(self.catShLine,grayCat.shape[0]):
			check = 0
			prev = 0
			for j in xrange(grayCat.shape[1]):
				if check == 0 and grayCat[i][j] != grayCat[0][0]:
					startCat[i] = j
					check = 1
				elif check == 1 and grayCat[i][j] == grayCat[0][0]:
					if prev != (j-1):
						endCat[i] = j
					prev = j
		
		output = np.zeros(userImg.shape)
		for i in xrange(self.userShLine,userImg.shape[0]-1):
			for j in xrange(startUser[i],endUser[i]):
				try:
					if grayCat[i + self.catShLine - self.userShLine][startCat[i + self.catShLine - self.userShLine] + j - startUser[i]] != 0:
						output[i][j] = catImg[i + self.catShLine - self.userShLine][startCat[i + self.catShLine - self.userShLine] + j - startUser[i]]
				except:
					pass
		
		return output

	def rightFit(self,userImg,catImg):

		grayUser = cv2.cvtColor(userImg,cv2.COLOR_BGR2GRAY)
		grayCat = cv2.cvtColor(catImg,cv2.COLOR_BGR2GRAY)
		self.userShLine = 0
		self.catShLine = 0
		check = 0
		for i in xrange(grayUser.shape[0]):
			for j in xrange(grayUser.shape[1]-1,-1,-1):
				if grayUser[i][j] != grayUser[0][0]:
					self.userShLine = i
					check = 1
					break
			if check != 0:
				break
		
		check = 0
		for i in xrange(grayCat.shape[0]):
			for j in xrange(grayCat.shape[1]-1,-1,-1):
				if grayCat[i][j] != grayCat[0][0]:
					self.catShLine = i
					check = 1
					break
			if check != 0:
				break
		
		startUser = [0]*grayUser.shape[0]
		startCat= [0]*grayCat.shape[0]
		endUser = [0]*grayUser.shape[0]
		endCat = [0]*grayCat.shape[0]

		for i in xrange(grayUser.shape[0]):
			check = 0
			prev = 0
			for j in xrange(grayUser.shape[1]-1,-1,-1):
				if check == 0 and grayUser[i][j] != grayUser[0][0]:
					startUser[i] = j
					check = 1
				elif check == 1 and grayUser[i][j] == grayUser[0][0]:
					if prev != (j+1):
						endUser[i] = j
					prev = j

		for i in xrange(grayCat.shape[0]):
			check = 0
			prev = 0
			for j in xrange(grayCat.shape[1]-1,-1,-1):
				if check == 0 and grayCat[i][j] != grayCat[0][0]:
					startCat[i] = j
					check = 1
				elif check == 1 and grayCat[i][j] == grayCat[0][0]:
					if prev != (j+1):
						endCat[i] = j
					prev = j
		
		output = np.zeros(userImg.shape)
		for i in xrange(userImg.shape[0]):
			for j in xrange(startUser[i]-1,endUser[i],-1):
				try:
					if grayCat[i + self.catShLine - self.userShLine][startCat[i + self.catShLine - self.userShLine] + j - startUser[i]] != 0  :
						output[i][j] = catImg[i + self.catShLine - self.userShLine][startCat[i + self.catShLine - self.userShLine] + j - startUser[i]]
				except:
					pass		
		return output

	def sleeveFit(self):
		self.resizeCat()		
		extra = 200
		leftUser = np.lib.pad(self.leftArmUser,((extra,extra),(extra,extra),(0,0)),'constant',constant_values=(0))
		rightUser = np.lib.pad(self.rightArmUser,((extra,extra),(extra,extra),(0,0)),'constant',constant_values=(0))
		leftCat = np.lib.pad(self.leftArmCat,((extra,extra),(extra,extra),(0,0)),'constant',constant_values=(0))
		rightCat = np.lib.pad(self.rightArmCat,((extra,extra),(extra,extra),(0,0)),'constant',constant_values=(0))

		leftUserRot,leftUserX,leftUserY,leftUserTheta = self.rotateNSave(leftUser,'left')
		rightUserRot,rightUserX,rightUserY,rightUserTheta = self.rotateNSave(rightUser,'right')
		leftCatRot,leftCatX,leftCatY,leftCatTheta = self.rotateNSave(leftCat,'left')
		rightCatRot,rightCatX,rightCatY,rightCatTheta = self.rotateNSave(rightCat,'right')

		#cv2.imwrite('debug/leftUserRot.jpg',leftUserRot)
		#cv2.imwrite('debug/rightUserRot.jpg',rightUserRot)
		#cv2.imwrite('debug/leftCatRot.jpg',leftCatRot)
		#cv2.imwrite('debug/rightCatRot.jpg',rightCatRot)

		leftUserFit = self.leftFit(leftUserRot,leftCatRot)
		rightUserFit = self.rightFit(rightUserRot,rightCatRot)

		#cv2.imwrite('debug/leftUserFit.jpg',leftUserFit)
		#cv2.imwrite('debug/rightUserFit.jpg',rightUserFit	)

		finalLeft = self.rotateImage(leftUserFit,-leftUserTheta,leftUserX,leftUserY)
		finalRight = self.rotateImage(rightUserFit,-rightUserTheta,rightUserX,rightUserY)

		return finalLeft, finalRight

	def finalFit(self,bodyFitOut,finalLeft,finalRight):
		for i in xrange(bodyFitOut.shape[0]):
			for j in xrange(bodyFitOut.shape[1]):
				if (finalLeft[i][j] != [0,0,0]).all():
					bodyFitOut[i][j] = finalLeft[i][j]
				if (finalRight[i][j] != [0,0,0]).all():
					bodyFitOut[i][j] = finalRight[i][j]
		return bodyFitOut
