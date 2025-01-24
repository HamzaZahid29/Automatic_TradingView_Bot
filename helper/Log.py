import sys
import os
# add main directoty of the project
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR)) 
from Database.connection import Connection

def insertlog(data):
    try:
        print(data)
        logcol = Connection.get_logs_col()
        result=logcol.insert_one(data)
        return result
    except Exception as e:
        print('got exception as ',e)    

