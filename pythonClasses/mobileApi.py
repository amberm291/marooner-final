#from master import attribute
from flask import Flask
from flask import json
from flask import request
from flask import Response
import json
from pprint import pprint
import base64
import cv2
import numpy as np
import pickle
app = Flask(__name__)

@app.route("/imageUpload" , methods=['POST'])
def imageUpload():
    #keyDict = request.form
    keyDict = request.get_json()
    img = keyDict['image']
    #userId = keyDict['userId']
    with open('userImg.jpg','wb') as imgfile:
        imgfile.write(base64.b64decode(img))
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route("/setMask", methods=['POST'])
def setMask():
    keyDict = request.get_json()
    bgdmodel = np.zeros((1,65),np.float64)
    fgdmodel = np.zeros((1,65),np.float64) 
    userImg = cv2.imread('userImg.jpg')
    if 'topX' in keyDict.keys():
        topX = int(keyDict['topX'])
        topY = int(keyDict['topY'])
        width = int(keyDict['width'])
        height = int(keyDict['height'])
        rect = (topX,topY,width,height)
        mask = np.zeros(userImg.shape[:2],dtype = np.uint8)
        cv2.grabCut(userImg,mask,rect,bgdmodel,fgdmodel,10,cv2.GC_INIT_WITH_RECT)
        np.save('mask',mask)
        pickle.dump(rect,open('userRect.p','wb'))
    else:
        rect = pickle.load(open('userRect.p','rb'))
        topX, topY, width, height = rect
        mask = np.load('mask.npy')
        
    
    fgPoints = []
    bgPoints = []
    for item in keyDict['foreground']:
        fgPoints.append((int(item['x']),int(item['y'])))

    for item in keyDict['background']:
        bgPoints.append((int(item['x']),int(item['y'])))
    
    for item in fgPoints:
        if topX < item[0] and item[0] < topX + width and topY < item[1] and item[1] < topY + height:
            mask[item[1]][item[0]] = 1

    for item in bgPoints:
        if topX < item[0] and item[0] < topX + width and topY < item[1] and item[1] < topY + height:
            mask[item[1]][item[0]] = 0

    cv2.imwrite('maskOut.jpg',img)
    cv2.grabCut(userImg,mask,rect,bgdmodel,fgdmodel,10,cv2.GC_INIT_WITH_MASK)

    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    output = userImg*mask2[:,:,np.newaxis]
    cv2.imwrite("debug/grabcutOutput.jpg",output)
    encodeImg = base64.b64encode(open('debug/grabcutOutput.jpg').read())
    result = {}
    result['img'] = encodeImg
    resp = Response(json.dumps(result),status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)
