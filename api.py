import fastapi
import logging
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
reserved_list =  []
avail_list = []

class Item(BaseModel):
    uid: str
    base64: str
    
class tokenItem(BaseModel):
    channelName: str
    token: str

class authItem(BaseModel):
    customerKey: str
    secretKey: str

class resItem(BaseModel):
    action: str
    timestamp : int

@app.get('/')
def home():
	return {"message": "U un ready"}

@app.post('/token')
async def createTokenfile(item: tokenItem):
	filename = '../token'
 
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

@app.get('/token')
async def getToken():
    filename = '../restapi/token'
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
        
@app.get('/agoratoken')
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

@app.post('/agoraauth')
async def getAgoraAuthentication(item: authItem):
	cKey = item.customerKey
	sKey = item.secretKey

	credentials = cKey + ":" + sKey
	base64_credentials = base64.b64encode(credentials.encode("utf8"))
	credential = base64_credentials.decode("utf8")

	print("Authentication is : ", credential)
 
	return JSONResponse({
        'auth' : 'basic ' + credential,
	})


@app.post('/reservation/available_date')
async def setAvailablelist(item: resItem):
	act = item.action
	ts = item.timestamp
	msg = ''
	global avail_list
 
	if (act=='add'):
		print("list append : ", ts)
		avail_list.append(ts)
		print("list : ", avail_list)
		msg = 'timestamp ' + str(ts) + ' added'
	elif (act=='modify'):
		print("test 2")
	elif (act=='delete'):
		print("test 3")
	else :
		print("test 4")
  
	return JSONResponse({
	    'msg' : msg
	})

@app.post('/reservation/add_reservation')
async def setReservation(item: resItem):
	act = item.action
	ts = item.timestamp
	msg = ''
	global reserved_list
 
	if (act=='add'):
		print("stored list: ", ts)
		reserved_list.append(ts)
		print("list : ", reserved_list)
		msg = 'timestamp ' + str(ts) + ' added'
	elif (act=='modify'):
		print("test 2")
	elif (act=='delete'):
		print("test 3")
	else :
		print("test 4")

	return JSONResponse({
        'msg' : msg 
	})

@app.get('/reservation/available_list')
async def getAvailablelist():
	return JSONResponse({
        'available' : avail_list
	})

@app.get('/reservation/reserved_list')
async def getReservedList():
	return JSONResponse({
        'reserved' : reserved_list
	})

@app.get('/debug/getList')
async def getList():
	return JSONResponse({
		'available' : avail_list,
        'reserved' : reserved_list
	})
 
@app.get('/debug/clearList')
async def getClearList():
	avail_list.clear()
	reserved_list.clear()
	return JSONResponse({
		'available' : avail_list,
        'reserved' : reserved_list
	})
 
