import cv2
import sys
from user import grabcut, userPreprocess
from catalogue import catPreprocess
from lower import lowerFit
from fit import userFit

if sys.argv[3] == "1":
	grabcutOutput = cv2.imread('debug/grabcutOutput.png') 
else:
	img = cv2.imread(sys.argv[1])
	grabInst = grabcut(img)
	grabcutOutput = grabInst.grabcut()
	cv2.imwrite("debug/grabcutOutput.png",grabcutOutput)

processInst = userPreprocess(grabcutOutput)
processInst.cropImg()
processOut = processInst.removeTurds()
cv2.imwrite('debug/processOut.png',processOut)

catImg = cv2.imread(sys.argv[2])
catInst = catPreprocess(catImg)
floodOut = catInst.flood(10)
cv2.imwrite('debug/floodOut.png',floodOut) 
cropFlood = catInst.cropImg(floodOut)
cv2.imwrite('debug/cropFlood.png',cropFlood)

lowInst = lowerFit(processOut,cropFlood)
lowInst.calcLowerLine()
lowInst.resizeCat()
finalOut = lowInst.fit()
cv2.imwrite('debug/finalOut.png',finalOut)

fitInst = userFit(processOut,cropFlood)
fitInst.setUserBox(processInst.returnUserBox())
output = fitInst.fittingOntoUser(finalOut,cv2.imread(sys.argv[1]))
cv2.imwrite('fittingOntoUser.png',output)