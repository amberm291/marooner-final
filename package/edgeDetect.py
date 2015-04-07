import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

img = cv2.imread(sys.argv[1],0)
edges = cv2.Canny(img,100,300)

cv2.imwrite( "canny.png", edges)
plt.show()