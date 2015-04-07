import cv2
import numpy as np
import sys
import math

def getBox(img):
	lx = ly = ux = uy = rx = ry = dx = dy= 0.0

	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if(ux == 0 and uy == 0):
				if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
					ux = j
					uy = i
		if(ux != 0 or uy != 0):
			break

	for i in range(img.shape[0]-1, -1, -1):
		for j in range(img.shape[1]):
			if(dx == 0 and dy == 0):
				if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
					dx = j
					dy = i
		if(dx != 0 or dy != 0):
			break

	for j in range(img.shape[1]):
		for i in range(img.shape[0]):
			if(lx == 0 and ly == 0):
				if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
					lx = j
					ly = i
		if(lx != 0 or ly != 0):
			break

	for j in range(img.shape[1]-1, -1, -1):
		for i in range(img.shape[0]):
			if(rx == 0 and ry == 0):
				if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
					rx = j
					ry = i
		if(rx != 0 or ry != 0):
			break


	return [lx, ly,rx, ry,ux, uy,dx, dy]

def rotateImage(img,theta,mid1,mid2,s):
	M = cv2.getRotationMatrix2D((mid1, mid2),theta,1)
	dst = cv2.warpAffine(img,M,(img.shape[1],img.shape[0]))
	extra = 200
	cropimg = dst[extra:dst.shape[0]-extra, extra:dst.shape[1]-extra]
	cv2.imwrite("finalrotate"+s + ".png", cropimg)

def shiftImage(img, a, b):
	img2 = np.zeros((img.shape[0], img.shape[1], 3))
	for i in range(img2.shape[0]):
		for j in range(img2.shape[1]):
			img2[i][j][0] = 0
			img2[i][j][1] = 0
			img2[i][j][2] = 0

	for i in range(0, b):
		for j in range(img.shape[0]):
			img2[j][img.shape[1]/2 + i - a][0] = img[j][i][0]
			img2[j][img.shape[1]/2 + i - a][1] = img[j][i][1]
			img2[j][img.shape[1]/2 + i - a][2] = img[j][i][2]

	cv2.imwrite('aaa.png', img2)
	return img2

def rotateNsave(img, s, p):
	lx, ly,rx, ry,ux, uy,dx, dy = getBox(img)
	#l1x, l1y,r1x, r1y,u1x, u1y,d1x, d1y = getBox(img_)

	check_inf = 0
	if(p == 0):	
		if(ux==lx):
			check_inf = 1
		else:
			m1 = (1.0*uy-ly)/(ux-lx)
		#m2 = (1.0*u1y-l1y)/(u1x-l1x)
	else:
		if(ux==rx):
			check_inf = 1
		else:
			m1 = (1.0*uy-ry)/(ux-rx)
		#m2 = (1.0*u1y-r1y)/(u1x-r1x)

	#img_ = shiftImage(img_, mid1, r1)
	mid1 = ux
	mid2 = uy

	if(check_inf == 0):
		theta = math.degrees(math.atan(m1))
	else:
		theta = 90
		if(p==1):
			theta = -90

	M = cv2.getRotationMatrix2D((mid1, mid2),theta,1)
	dst = cv2.warpAffine(img,M,(img.shape[1],img.shape[0]))
	cv2.imwrite("rotate"+s+".png", dst)
	return dst,ux,uy,theta


img = cv2.imread(sys.argv[1],1)
img_ = cv2.imread(sys.argv[2],1)
img2 = cv2.imread(sys.argv[3],1)
img2_ = cv2.imread(sys.argv[4],1)

hU = img.shape[0]
wU = img.shape[1]
hC = img2.shape[0]
wC = img2.shape[1]

extra = 200

n_img = np.zeros((hU+2*extra, wU+2*extra, 3))
n_img_ = np.zeros((hU+2*extra, wU+2*extra, 3))
n_img2 = np.zeros((hC+2*extra, wC+2*extra, 3))
n_img2_ = np.zeros((hC+2*extra, wC+2*extra, 3))

for i in range(0, hU):
	for j in range(0, wU):
		n_img[i+extra][j+extra] = img[i][j]
		n_img_[i+extra][j+extra] = img_[i][j]

for i in range(0, hC):
	for j in range(0, wC):
		n_img2[i+extra][j+extra] = img2[i][j]
		n_img2_[i+extra][j+extra] = img2_[i][j]

img = n_img
img_ = n_img_
img2 = n_img2
img2_ = n_img2_



img,ux,uy,theta = rotateNsave(img, "leftUser", 0)
img_,ux_,uy_,theta_ = rotateNsave(img_, "rightUser", 1)
img2,ux2,uy2,theta2 = rotateNsave(img2, "leftProd", 0)
img2_,ux2_,uy2_,theta2_ = rotateNsave(img2_, "rightProd", 1)


def leftfit(img,img2):

	h = img.shape[0]
	w = img.shape[1]

	check = 0

	L = 0
	L1 = 0

	for j in range(img.shape[1]):
		for i in range(img.shape[0]):
			if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
				L = j
				check=1
				break
		if (check!=0):
			break
	check=0
	for j in range(img2.shape[1]):
		for i in range(img2.shape[0]):
			if(img2[i][j][0] != img2[0][0][0] or img2[i][j][1] != img2[0][0][1] or img2[i][j][2] != img2[0][0][2]):
				L2 = j
				check=1
				break
		if (check!=0):
			break
	start = [0 for i in range(img.shape[1])]
	start2= [0 for i in range(img2.shape[1])]
	end = [0 for i in range(img.shape[1])]
	end2= [0 for i in range(img2.shape[1])]
	for j in range(L,img.shape[1]):
		check=0
		for i in range(img.shape[0]):
			if(check==0 and (img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2])):
				start[j]=i
				check=1
			elif(check==1 and (img[i][j][0] == img[0][0][0] and img[i][j][1] == img[0][0][1] and img[i][j][2] == img[0][0][2])):
				end[j]=i
				break
	for j in range(L2,img2.shape[1]):
		check=0
		for i in range(img2.shape[0]):
			if(check==0 and (img2[i][j][0] != img2[0][0][0] or img2[i][j][1] != img2[0][0][1] or img2[i][j][2] != img2[0][0][2])):
				start2[j]=i
				check=1
			elif(check==1 and (img2[i][j][0] == img2[0][0][0] and img2[i][j][1] == img2[0][0][1] and img2[i][j][2] == img2[0][0][2])):
				end2[j]=i
				break

	pp = [0,0,0]
	for j in range(L,img.shape[1]):
		for i in range(start[j],end[j]+1):
			try:
				if(img2[start2[j+L2-L]+i-start[j]][j+L2-L][0]!=0 or img2[start2[j+L2-L]+i-start[j]][j+L2-L][1]!=0 or img2[start2[j+L2-L]+i-start[j]][j+L2-L][2]!=0):
					img[i][j]=img2[start2[j+L2-L]+i-start[j]][j+L2-L]
			except:
				pass
	cv2.imwrite("templeft.png",img)
	return img

def rightfit(img,img2):
	h = img.shape[0]
	w = img.shape[1]

	check = 0

	R = 0
	Rr = 0

	for j in range(img.shape[1]-1,-1,-1):
		for i in range(img.shape[0]):
			if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
				R = j
				check=1
				break
		if (check!=0):
			break
	check=0
	for j in range(img2.shape[1]-1,-1,-1):
		for i in range(img2.shape[0]):
			if(img2[i][j][0] != img2[0][0][0] or img2[i][j][1] != img2[0][0][1] or img2[i][j][2] != img2[0][0][2]):
				R2 = j
				check=1
				break
		if (check!=0):
			break
	start = [0 for i in range(img.shape[1])]
	start2= [0 for i in range(img2.shape[1])]
	end = [0 for i in range(img.shape[1])]
	end2= [0 for i in range(img2.shape[1])]
	for j in range(0,R):
		check=0
		for i in range(img.shape[0]):
			if(check==0 and (img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2])):
				start[j]=i
				check=1
			elif(check==1 and (img[i][j][0] == img[0][0][0] and img[i][j][1] == img[0][0][1] and img[i][j][2] == img[0][0][2])):
				end[j]=i
				break
	for j in range(0,R2):
		check=0
		for i in range(img2.shape[0]):
			if(check==0 and (img2[i][j][0] != img2[0][0][0] or img2[i][j][1] != img2[0][0][1] or img2[i][j][2] != img2[0][0][2])):
				start2[j]=i
				check=1
			elif(check==1 and (img2[i][j][0] == img2[0][0][0] and img2[i][j][1] == img2[0][0][1] and img2[i][j][2] == img2[0][0][2])):
				end2[j]=i
				break

	pp = [0,0,0]
	for j in range(R,0,-1):
		for i in range(start[j],end[j]+1):
			try:
				if(img2[start2[j+R2-R]+i-start[j]][j+R2-R][0]!=0 or img2[start2[j+R2-R]+i-start[j]][j+R2-R][1]!=0 or img2[start2[j+R2-R]+i-start[j]][j+R2-R][2]!=0):
					img[i][j]=img2[start2[j+R2-R]+i-start[j]][j+R2-R]
			except:
				pass
	cv2.imwrite("tempright.png",img)
	return img


img = leftfit(img,img2)

img_ = rightfit(img_,img2_)

rotateImage(img,-theta,ux,uy,"left")
rotateImage(img_,-theta_,ux_,uy_,"right")
