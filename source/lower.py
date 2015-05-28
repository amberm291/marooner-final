import cv2
import numpy as np
import Queue

class lowerFit:

	def __init__(self,userImg,catImg):
		self.userImg = userImg
		self.catImg = catImg
		self.vRatio = 1
		self.hRatio = 1.2
		self.userLine = 0
		self.catLine = 0

	def calcLowerLine(self):
		grayUser = cv2.cvtColor(self.userImg,cv2.COLOR_BGR2GRAY)
		for i in xrange((2*self.userImg.shape[0])/3,0,-1):
			count = 0
			for j in xrange(1, self.userImg.shape[1]):
				if grayUser[i][j-1] != 0 and grayUser[i][j] == 0:
					count += 1
			j = grayUser.shape[1]
			if grayUser[i][j-1] != 0:
				count += 1
			if count == 1:
				self.userLine = i+1
				break

		grayCat = cv2.cvtColor(self.catImg,cv2.COLOR_BGR2GRAY)
		for i in xrange((2*self.catImg.shape[0])/3,0,-1):
			count=0
			for j in xrange(1, self.catImg.shape[1]):
				if grayCat[i][j-1] != grayCat[0][0] and grayCat[i][j] == grayCat[0][0]:
					count += 1
			j = grayCat.shape[1]
			if grayCat[i][j-1] != grayCat[0][0]:
				count += 1
			if count == 1:
				self.catLine = i+1
				break


	def resizeCat(self):
		oldLen = self.catImg.shape[0]
		userLine = self.catImg.shape[0] - self.userLine
		catLine = self.userImg.shape[0] - self.catLine

		diff = abs(userLine - catLine)
		self.vRatio += float(diff)/userLine

		self.catImg = cv2.resize(self.catImg,(int(self.hRatio*self.userImg.shape[1]),int(self.vRatio*self.userImg.shape[0])),interpolation=cv2.INTER_NEAREST)
		#cv2.imwrite('debug/resizedCat.png',self.catImg)
		self.catLine *= float(self.catImg.shape[0])/oldLen
		self.catLine = int(self.catLine)

	def fit(self):
		startUser = [0]*self.userImg.shape[0]
		endUser = [0]*self.userImg.shape[0]
		startCat = [0]*self.catImg.shape[0]
		endCat = [0]*self.catImg.shape[0]
		leftUser = [0]*self.userImg.shape[0]
		rightUser = [0]*self.userImg.shape[0]
		leftCat = [0]*self.catImg.shape[0]
		rightCat = [0]*self.catImg.shape[0]

		grayUser = cv2.cvtColor(self.userImg,cv2.COLOR_BGR2GRAY)
		grayCat = cv2.cvtColor(self.catImg,cv2.COLOR_BGR2GRAY)
		finalOut = self.userImg
		
		first = 0
		end = 0

		for i in xrange(0, grayUser.shape[0]):
			for j in xrange(0, grayUser.shape[1]):
				if grayUser[i][j] != 0:
					first=i
					break
			if first != 0:
				break

		for i in xrange(grayUser.shape[0]-1,0,-1):
			for j in xrange(0, grayUser.shape[1]):
				if grayUser[i][j]!=0:
					end=i
					break
			if end != 0:
				break

		for i in xrange(0, grayUser.shape[0]):
			for j in xrange(0, grayUser.shape[1]):
				if grayUser[i][j] != 0:
					startUser[i]=j
					break
				if j == grayUser.shape[1]:
					startUser[i]=j
					break

		for i in xrange(0, grayUser.shape[0]):
			for j in xrange(grayUser.shape[1]-1,0,-1):
				if grayUser[i][j] != 0:
					endUser[i]=j
					break
				if j == 0:
					endUser[i]=startUser[i]

		for i in xrange(0, grayCat.shape[0]):
			for j in xrange(0, grayCat.shape[1]):
				if grayCat[i][j] !=0:
					startCat[i]=j
					break
				if j == grayUser.shape[1]:
					startCat[i]=j
					break

		for i in xrange(0, grayCat.shape[0]):
			for j in xrange(grayCat.shape[1]-1,0,-1):
				if grayCat[i][j] != 0:
					endCat[i]=j
					break
				if j == 0:
					endCat[i]=startCat[i]

		for i in xrange(self.userLine+1,grayUser.shape[0]):
			for j in xrange(startUser[i]+1,grayUser.shape[1]):
				if grayUser[i][j] == 0:
					leftUser[i]=j-1
					break
			for j in xrange(endUser[i]-1,0,-1):
				if grayUser[i][j] == 0:
					rightUser[i]=j
					break

		for i in xrange(self.catLine+1,grayCat.shape[0]):
			for j in xrange(startCat[i]+1,grayUser.shape[1]):
				if grayCat[i][j] == 0:
					leftCat[i]=j-1
					break
			for j in xrange(endCat[i]-1,startCat[i],-1):
				if grayCat[i][j] == 0:
					rightCat[i]=j
					break

		pt1 = leftUser[self.userLine+1]
		pt2 = leftCat[self.catLine+1]

		for i in xrange(self.userLine,first-1,-1):
			for j in xrange(pt1,startUser[i]-1,-1):
				if finalOut[i][j][0]!=0 or finalOut[i][j][1]!=0 or finalOut[i][j][2]!=0:
					try:
						finalOut[i][j] = self.catImg[self.catLine+i-self.userLine][pt2+j-pt1]
					except:
						pass
				
			for j in xrange(pt1,endUser[i]+1):
				if finalOut[i][j][0]!=0 or finalOut[i][j][1]!=0 or finalOut[i][j][2]!=0:
					try:
						finalOut[i][j] = self.catImg[self.catLine+i-self.userLine][pt2+j-pt1]
					except:
						pass

		for i in xrange(self.userLine+1,end+1):
			for j in xrange(leftUser[i],startUser[i]-1,-1):
				try:
					finalOut[i][j] = self.catImg[self.catLine+i-self.userLine][leftCat[self.catLine+i-self.userLine]+j-leftUser[i]]
				except:
					pass
			
			for j in xrange(rightUser[i]+1,endUser[i]+1):
				try:
					finalOut[i][j] = self.catImg[self.catLine+i-self.userLine][rightCat[self.catLine+i-self.userLine]+j-rightUser[i]]
				except:
					pass

		return finalOut
