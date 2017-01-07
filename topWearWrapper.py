from source.user import grabcut, userPreprocess 
import cv2
import os
import sys
from source.catalogue import catPreprocess
from source.fit import userFit

if not os.path.exists('debug/'):
	os.makedirs('debug/')

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

processInst.segImage(processOut)
LU, RU = processInst.getSegLines()

leftArmUser = processInst.armSegment(processOut,'left')
cv2.imwrite('debug/leftArmUser.png',leftArmUser)
rightArmUser = processInst.armSegment(processOut,'right')
cv2.imwrite('debug/rightArmUser.png',rightArmUser)
#userBox = processInst.returnUserBox()

catImg = cv2.imread(sys.argv[2])
catInst = catPreprocess(catImg)
floodOut = catInst.edgeDetect()
cv2.imwrite("debug/floodOut.png",floodOut)
cropFlood = catInst.cropImg(floodOut)
catInst.segImage(cropFlood)
LC, RC = catInst.getSegLines()
cv2.imwrite("debug/cropFloodOut.png",cropFlood)

rightArmCat = catInst.armSegment(cropFlood,'right')
cv2.imwrite('debug/rightArmCat.png',rightArmCat)
leftArmCat = catInst.armSegment(cropFlood,'left')
cv2.imwrite('debug/leftArmCat.png',leftArmCat)
#catResizeLine = catInst.getCatResizeLine(cropFlood)


fitInst = userFit(processOut,cropFlood)
fitInst.setSegLines(LC,RC,LU,RU)
#fitInst.setResizeLines(userResizeLine,catResizeLine)
colorUserOut = fitInst.colorUser()
cv2.imwrite('debug/colorUserOut.png',colorUserOut)
fitInst.setUserArm(leftArmUser,rightArmUser)
fitInst.setCatArm(leftArmCat,rightArmCat)
fitLeft, fitRight = fitInst.sleeveFit()
cv2.imwrite('debug/fitLeft.png',fitLeft)
cv2.imwrite('debug/fitRight.png',fitRight)
bodyFitOut = fitInst.bodyFit(colorUserOut)
cv2.imwrite('debug/bodyFitOut.png',bodyFitOut)
finalFit = fitInst.finalFit(bodyFitOut,fitLeft,fitRight)
cv2.imwrite('debug/finalFit.png',finalFit)
#finalFit = fitInst.sleeveFit(bodyFitOut)
#cv2.imwrite('finalFit.png',finalFit)
fitInst.setUserBox(processInst.returnUserBox())
output = fitInst.fittingOntoUser(finalFit,cv2.imread(sys.argv[1]))
cv2.imwrite('fittingOntoUser.jpg',output)
