import cv2
import numpy as np
import sys
import math

'''
Returns top, right, bottom and left coordinates (x,y) of segmented sleeve
'''
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

'''
Rotates img by theta about (mid1, mid2) where s is the string used in the name of final image saved
'''
def rotateImage(img,theta,mid1,mid2,s):
	M = cv2.getRotationMatrix2D((mid1, mid2),theta,1)
	dst = cv2.warpAffine(img,M,(img.shape[1],img.shape[0]), flags= cv2.INTER_NEAREST)
	extra = 200
	cropimg = dst[extra:dst.shape[0]-extra, extra:dst.shape[1]-extra]
	cv2.imwrite("finalrotate"+s + ".png", cropimg)

'''
NOT USED
'''
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

'''
p==0 means left and p == 1 means right sleeve
For left sleeve: computes theta by top (x,y) and left (x,y) of the segmented sleeve
then computes slope. THen take is tan inverse to get theta in degrees and finally rotates and saves
the rotated sleeve image.
For right sleeve: computes theta by top (x,y) and right (x,y) ....same....
'''
def rotateNsave(img, s, p):
	lx, ly,rx, ry,ux, uy,dx, dy = getBox(img)
	#l1x, l1y,r1x, r1y,u1x, u1y,d1x, d1y = getBox(img_)

	print lx, ly, rx, ry, ux, uy, dx, dy
	check_inf = 0
	if(p == 0):	
		#check if perpendicular n prevents div by zero
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
	dst = cv2.warpAffine(img,M,(img.shape[1],img.shape[0]),flags= cv2.INTER_NEAREST)
	cv2.imwrite("rotate"+s+".png", dst)
	return dst,ux,uy,theta

def leftfit(img,img2):

	h = img.shape[0]
	w = img.shape[1]

	check = 0

	L = 0
	L2 = 0
	'''
		find topmost non black pixel for user sleeve and hence the corresponding row is stored in L
	'''
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
				L = i
				check=1
				break
		if (check!=0):
			break
	check=0
	'''
		find topmost non black pixel for catalogue sleeve and hence the corresponding row is stored in L2
	'''
	for i in range(img2.shape[0]):
		for j in range(img2.shape[1]):
			if(img2[i][j][0] != img2[0][0][0] or img2[i][j][1] != img2[0][0][1] or img2[i][j][2] != img2[0][0][2]):
				L2 = i
				check=1
				break
		if (check!=0):
			break
	start = [0 for i in range(img.shape[0])]
	start2= [0 for i in range(img2.shape[0])]
	end = [0 for i in range(img.shape[0])]
	end2= [0 for i in range(img2.shape[0])]
	'''
		Store non black pixels of each row in user sleeve from row L till bottom
	'''
	for i in range(L,img.shape[0]):
		check=0
		prev = 0
		for j in range(img.shape[1]):
			if(check==0 and (img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2])):
				start[i]=j
				check=1
			elif(check==1 and (img[i][j][0] == img[0][0][0] and img[i][j][1] == img[0][0][1] and img[i][j][2] == img[0][0][2])):
				if(prev!=(j-1)):
					end[i]=j
				prev = j
	'''
		Store non black pixels of each row in catalogue sleeve from row L2 till bottom
	'''
	for i in range(L2,img2.shape[0]):
		check=0
		prev=0
		for j in range(img2.shape[1]):
			if(check==0 and (img2[i][j][0] != img2[0][0][0] or img2[i][j][1] != img2[0][0][1] or img2[i][j][2] != img2[0][0][2])):
				start2[i]=j
				check=1
			elif(check==1 and (img2[i][j][0] == img2[0][0][0] and img2[i][j][1] == img2[0][0][1] and img2[i][j][2] == img2[0][0][2])):
				if(prev!=(j-1)):
					end2[i]=j
				prev = j
	'''
		Row wise fitting. Superimposing each pixel stored from start[i+offset] to end[i+offset] on start[i] to end[i]
		where offset is L2-L
	'''
	pp = [0,0,0]
	img3 = np.zeros((img.shape[0],img.shape[1],3))
	for i in range(L,img.shape[0]-1):
		for j in range(start[i],end[i]):
			try:
				if(img2[i+L2-L][start2[i+L2-L]+j-start[i]][0]!=0 or img2[i+L2-L][start2[i+L2-L]+j-start[i]][1]!=0 or img2[i+L2-L][start2[i+L2-L]+j-start[i]][2]!=0):
					img3[i][j]=img2[i+L2-L][start2[i+L2-L]+j-start[i]]
			except:
				pass
	cv2.imwrite("templeft.png",img3)
	return img3

'''
	Right sleeve fitting analogous to left fitting
'''
def rightfit(img,img2):
	h = img.shape[0]
	w = img.shape[1]

	check = 0

	R = 0
	R2 = 0

	for i in range(img.shape[0]):
		for j in range(img.shape[1]-1,-1,-1):
			if(img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2]):
				R = i
				check=1
				break
		if (check!=0):
			break
	check=0
	for i in range(img2.shape[0]):
		for j in range(img2.shape[1]-1,-1,-1):
			if(img2[i][j][0] != img2[0][0][0] or img2[i][j][1] != img2[0][0][1] or img2[i][j][2] != img2[0][0][2]):
				R2 = i
				check=1
				break
		if (check!=0):
			break
	start = [0 for i in range(img.shape[0])]
	start2= [0 for i in range(img2.shape[0])]
	end = [0 for i in range(img.shape[0])]
	end2= [0 for i in range(img2.shape[0])]
	for i in range(img.shape[0]):
		check=0
		prev = 0
		for j in range(img.shape[1]-1,-1,-1):
			if(check==0 and (img[i][j][0] != img[0][0][0] or img[i][j][1] != img[0][0][1] or img[i][j][2] != img[0][0][2])):
				start[i]=j
				check=1
			elif(check==1 and (img[i][j][0] == img[0][0][0] and img[i][j][1] == img[0][0][1] and img[i][j][2] == img[0][0][2])):
				if(prev!=j+1):
					end[i]=j
				prev=j
	for i in range(img2.shape[0]):
		check=0
		prev=0
		for j in range(img2.shape[1]-1,-1,-1):
			if(check==0 and (img2[i][j][0] != img2[0][0][0] or img2[i][j][1] != img2[0][0][1] or img2[i][j][2] != img2[0][0][2])):
				start2[i]=j
				check=1
			elif(check==1 and (img2[i][j][0] == img2[0][0][0] and img2[i][j][1] == img2[0][0][1] and img2[i][j][2] == img2[0][0][2])):
				if(prev!=j+1):
					end2[i]=j
				prev=j

	pp = [0,0,0]
	img3 = np.zeros((img.shape[0],img.shape[1],3))
	for i in range(img.shape[0]):
		for j in range(start[i]-1,end[i],-1):
			try:
				if(img2[i+R2-R][start2[i+R2-R]+j-start[i]][0]!=0 or img2[i+R2-R][start2[i+R2-R]+j-start[i]][1]!=0 or img2[i+R2-R][start2[i+R2-R]+j-start[i]][2]!=0):
					img3[i][j]=img2[i+R2-R][start2[i+R2-R]+j-start[i]]
			except:
				pass
	cv2.imwrite("tempright.png",img3)
	return img3


img = cv2.imread(sys.argv[1],1)
img_ = cv2.imread(sys.argv[2],1)
img2 = cv2.imread(sys.argv[3],1)
img2_ = cv2.imread(sys.argv[4],1)

hU = img.shape[0]
wU = img.shape[1]
hC = img2.shape[0]
wC = img2.shape[1]

extra = 200
#appending extra rows to prevent rotated sleeve to go out of frame
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

#rotate sleeve
img,ux,uy,theta = rotateNsave(img, "leftUser", 0)
img_,ux_,uy_,theta_ = rotateNsave(img_, "rightUser", 1)
img2,ux2,uy2,theta2 = rotateNsave(img2, "leftProd", 0)
img2_,ux2_,uy2_,theta2_ = rotateNsave(img2_, "rightProd", 1)

#fit sleeve
img = leftfit(img,img2)
img_ = rightfit(img_,img2_)

#rotate back to same position that's why minus theta
rotateImage(img,-theta,ux,uy,"left")
rotateImage(img_,-theta_,ux_,uy_,"right")
