import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],1)
img2 = cv2.imread(sys.argv[2],1)
ratio=0.7
img2 = cv2.resize(img2, (int(ratio*img.shape[1]), int(ratio*img.shape[0])),interpolation=cv2.INTER_NEAREST)

cv2.imwrite("resized" + sys.argv[2], img2)
