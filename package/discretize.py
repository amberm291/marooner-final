import numpy as np
import cv2
import sys

im = cv2.imread(sys.argv[1])

n = int(sys.argv[2])   # Number of levels of quantization
opt = sys.argv[3]
if(opt=="hd"):
	cv2.imwrite('discretized.png', im)
else:
	indices = np.arange(0,256)   # List of all colors 

	divider = np.linspace(0,255,n+1)[1] # we get a divider

	quantiz = np.int0(np.linspace(0,255,n)) # we get quantization colors

	color_levels = np.clip(np.int0(indices/divider),0,n-1) # color levels 0,1,2..

	palette = quantiz[color_levels] # Creating the palette

	im2 = palette[im]  # Applying palette on image

	im2 = cv2.convertScaleAbs(im2) # Converting image back to uint8

	cv2.imwrite('discretized.png', im2)