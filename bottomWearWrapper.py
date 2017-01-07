from source.user import grabcut, userPreprocess 
import cv2
import os
import sys
from source.catalogue import catPreprocess
from source.fit import userFit
from source.lower import lowerFit

if not os.path.exists('debug/'):
	os.makedirs('debug/')

if sys.argv[3] == "1":
	grabcutOutput = cv2.imread('debug/grabcutOutputLower.png') 
else:
	img = cv2.imread(sys.argv[1])
	grabInst = grabcut(img)
	grabcutOutput = grabInst.grabcut()
	cv2.imwrite("debug/grabcutOutputLower.png",grabcutOutput)

processInst = userPreprocess(grabcutOutput)
processInst.cropImg()
processOut = processInst.removeTurds()

catImg = cv2.imread(sys.argv[2])
catInst = catPreprocess(catImg)
floodOut = catInst.edgeDetect(threshold=220)
cv2.imwrite("debug/floodOutLower.png",floodOut)
cropFlood = catInst.cropImg(floodOut)
cv2.imwrite("debug/cropFloodOutLower.png",cropFlood)

lowInst = lowerFit(processOut,cropFlood)
lowInst.calcLowerLine()
lowInst.resizeCat()
finalOut = lowInst.fit()
fitInst = userFit(processOut,cropFlood)
userBox = processInst.returnUserBox()
fitInst.setUserBox(userBox)
output = fitInst.fittingOntoUser(finalOut,cv2.imread(sys.argv[1]))
cv2.imwrite('fittingOntoUserLower.jpg',output)
