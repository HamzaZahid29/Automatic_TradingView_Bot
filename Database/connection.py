from pymongo import MongoClient
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR)) 
from config import mongouri
import certifi

def connection():
    try:
        if not mongouri:
            raise ValueError('mongouri missing')
        ca=certifi.where()    
        client=MongoClient(mongouri,tls=True,tlsCAFile=ca,serverSelectionTimeoutMS=50000)
        db=client['tradeView']
        return db
    except Exception as e:
        print('Found Error while Connecting database',e)    
