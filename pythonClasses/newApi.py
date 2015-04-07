#from master import attribute
from flask import Flask
from flask import json
from flask import request
from flask import Response
from pprint import pprint
import base64
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/imageUpload" , methods=['POST'])
def imageUpload():
    keyDict = request.form
    print keyDict['topX']

    cWidth = int(keyDict['width'])
    #keyDict = request.get_json()
    
    img = keyDict['userImString']
    
    img = img[22:]
    with open('userImg.jpg','wb') as imgfile:
        imgfile.write(base64.b64decode(img))
    
    userImg = cv2.imread('userImg.jpg')
    topX = (userImg.shape[1]*int(keyDict['topX']))/cWidth
    topY = (userImg.shape[0]*int(keyDict['topY']))/720
    botX = (userImg.shape[1]*int(keyDict['bottomX']))/cWidth
    botY = (userImg.shape[0]*int(keyDict['bottomY']))/720
    if userImg.shape[0] > 720:
        height = userImg.shape[0]
        width = userImg.shape[1]
        userImg = cv2.resize(userImg,(int(userImg.shape[1]*720)/userImg.shape[0],int(userImg.shape[0]*720)/userImg.shape[0]),interpolation=cv2.INTER_NEAREST)
        cv2.imwrite('userImg.jpg',userImg)
        topX = topX*userImg.shape[1]/width
        topY = topY*userImg.shape[0]/height
        botX = botX*userImg.shape[1]/width
        botY = botY*userImg.shape[0]/height
    rect = (topX,topY,botX-topX,botY-topY)
    mask = np.zeros(userImg.shape[:2],dtype = np.uint8)
    bgdmodel = np.zeros((1,65),np.float64)
    fgdmodel = np.zeros((1,65),np.float64)   

    cv2.grabCut(userImg,mask,rect,bgdmodel,fgdmodel,10,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    output = userImg*mask2[:,:,np.newaxis]   
    
    np.save('debug/mask',mask)
    cv2.imwrite("debug/grabcutOutput.png",output)
    #image_file = open("debug/grabcutOutput.png", "rb") 

    #encoded_string = base64.b64encode(image_file.read())
    #result = {}
    #result['img'] = encoded_string
    resp = Response(status=200)
    #image_file.close()
    return resp

@app.route("/setMask" , methods=['POST'])
def setMask():
    keyDict = request.form
    mask = keyDict['mask']
    mask = mask[22:]
    #' '.join(img.split())
    #img.replace(' ','+')
    with open('debug/newMask.png','wb') as imgfile:
        imgfile.write(base64.b64decode(mask))
    
    newMask = cv2.imread('debug/newMask.png')
    userImg = cv2.imread('userImg.jpg')
    
    mask = np.load('debug/mask.npy')
    print mask.shape, newMask.shape
    for i in xrange(newMask.shape[0]):
        for j in xrange(newMask.shape[1]):
            if (newMask[i][j] == [0,0,0]).all():
                mask[i][j] = 0
            elif (newMask[i][j] == [0,255,0]).all():
                mask[i][j] = 1
    
    bgdmodel = np.zeros((1,65),np.float64)
    fgdmodel = np.zeros((1,65),np.float64)   
    rect = None
    cv2.grabCut(userImg,mask,rect,bgdmodel,fgdmodel,10,cv2.GC_INIT_WITH_MASK)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    output = userImg*mask2[:,:,np.newaxis]   
    
    np.save('debug/mask',mask)    
    cv2.imwrite("debug/grabcutOutput.png",output)
    image_file = open("debug/grabcutOutput.png", "rb") 

    encoded_string = base64.b64encode(image_file.read())
    result = {}
    result['img'] = encoded_string
    resp = Response(json.dumps(result), status=200, mimetype='application/json')
    image_file.close()
    return resp

@app.route("/getUser" , methods=['GET'])
def getUser():
    return base64.b64encode(open('debug/grabcutOutput.png').read())

if __name__ == "__main__":
    app.run(host='10.0.2.90',port=8000,debug=True)
