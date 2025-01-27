# using class base structure
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from pymongo import MongoClient
from Database.connection import Connection

# create function to get qunatity from database
class getQuanity:
    @classmethod
    def Extract_Quantity_TYPE(cls):
        try:
            db=Connection.get_key_col()
            key_col=db.find()
            for col in key_col:
                qunatity=col.get('quantity')
                type=col.get('type')
                return {'qunatity':qunatity,'type':type }  
        except Exception as e:
            print('Got An Exception in Extract_Quantity_TYPE()',e) 

def mongodata():
    trade=getQuanity()            
    quanity=trade.Extract_Quantity_TYPE()
    return quanity

      