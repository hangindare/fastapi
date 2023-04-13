import fastapi
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import Optional
from starlette.responses import JSONResponse
import time
from agora_token_builder import RtcTokenBuilder

import base64
import os.path

from fastapi import File, UploadFile
        
app = fastapi.FastAPI()

class Item(BaseModel):
    uid: str
    base64: str
    
class tokenItem(BaseModel):
    channelName: str
    token: str

@app.get('/')
def home():
	return {"message": "U un ready"}

@app.get('/JED/')
async def getData():
	return "jed"

@app.post('/token/')
async def createTokenfile(item: tokenItem):
	filename = 'c:/python/restapi/token'
 
	# jsondata = jsonable_encoder(item)
	# print(jsondata)
 
	with open(filename, 'w') as f:
		chname = item.channelName + '\n'
		token = item.token
		f.write(chname)
		f.write(token)
		msg = "token stored"

	return JSONResponse({
			'msg' : msg
	})

@app.get('/token/')
async def getToken():
    filename = 'c:/python/restapi/token'
    if not os.path.isfile(filename):
        err = 'no token info'
        return JSONResponse({
			'msg' : err
		})
    
    with open(filename, 'r') as f:
        chname = f.readline()[:-1]
        token = f.readline()
        return JSONResponse({
            'channelName' : chname,
            'token' : token
		})
        
@app.get('/agoratoken/')
async def getAgoraToken():
	appId = "4df65f62e6cd41e4938f42c10a8abf5b"
	appCertificate = "b35d2a23081f4671a7a454c0b61d7dd8"
	chname = "vacumm"
	account = "jaehyuk1220@gmail.com"
	uId = 0
	expirationTimeInSeconds = 60 * 60 * 24
    
	current_ts = int (time.time())
	ts = current_ts + expirationTimeInSeconds
 
	token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, chname, uId, 1, ts)
 
	print("token is : ", token)
	return JSONResponse({
        'channelName' : chname,
        'token' : token
	})
	