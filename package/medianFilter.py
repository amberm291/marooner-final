import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img3 = cv2.imread(sys.argv[1],1)

L = int(raw_input())
R = int(raw_input())
H = int(raw_input())
L = L + 20
R = R - 20
H = H - 5
hMargin = 5
vMargin = 5
medsize = int(raw_input())
shift = medsize/2

startpix = []
endpix = []
startpix2 = []
endpix2 = []

for i in range(H-hMargin, H+hMargin):
	for j in range(0, img.shape[1]):
		if(i >= 0 and i < img.shape[0] and (j <= L or j >= R)):
			rpix = []
			gpix = []
			bpix = []
			for k in range(i-shift, i+1+shift):
				for l in range(j-shift, j+1+shift):
					if(k >= 0 and l >= 0 and k < img.shape[0] and l < img.shape[1]):
						rpix.append(img[k][l][0])
						gpix.append(img[k][l][1])
						bpix.append(img[k][l][2])
			rpix.sort()
			gpix.sort()
			bpix.sort()
			img3[i][j][0] = rpix[int((medsize*medsize)/2)]
			img3[i][j][1] = gpix[int((medsize*medsize)/2)]
			img3[i][j][2] = bpix[int((medsize*medsize)/2)]


for i in range(0, H):
	for j in range(0, L+vMargin):
		if(j >= 0 and j < img.shape[1]):
                        if(img[i][j][0]!=0 or img[i][j][1] != 0 or img[i][j][2]!=0):
				rpix = []
				gpix = []
				bpix = []
				for k in range(i-shift, i+1+shift):
					for l in range(j-shift, j+1+shift):
						if(k >= 0 and l >= 0 and k < img.shape[0] and l < img.shape[1]):
							rpix.append(img[k][l][0])
							gpix.append(img[k][l][1])
							bpix.append(img[k][l][2])
				rpix.sort()
				gpix.sort()
				bpix.sort()
                        	img3[i][j][0] = rpix[int((medsize*medsize)/2)]
                        	img3[i][j][1] = gpix[int((medsize*medsize)/2)]
                        	img3[i][j][2] = bpix[int((medsize*medsize)/2)]

for i in range(0, H):
	for j in range(R-vMargin, img.shape[1]):
		if(j >= 0 and j < img.shape[1]):
                        if(img[i][j][0]!=0 or img[i][j][1] != 0 or img[i][j][2]!=0):
				rpix = []
				gpix = []
				bpix = []
				for k in range(i-shift, i+1+shift):
					for l in range(j-shift, j+1+shift):
						if(k >= 0 and l >= 0 and k < img.shape[0] and l < img.shape[1]):
							rpix.append(img[k][l][0])
							gpix.append(img[k][l][1])
							bpix.append(img[k][l][2])
				rpix.sort()
				gpix.sort()
				bpix.sort()
                        	img3[i][j][0] = rpix[int((medsize*medsize)/2)]
                		img3[i][j][1] = gpix[int((medsize*medsize)/2)]
        			img3[i][j][2] = bpix[int((medsize*medsize)/2)]


cv2.imwrite("medianFiltered.png", img3)
