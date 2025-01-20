from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import sys
# add main directoty of the project
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR)) 
from Database.connection import connection
from keymanagement.schema.keyschema import keySchema
from bson import ObjectId
from marshmallow import ValidationError

app=Flask(__name__)
CORS(app)
api_key_schema=keySchema()

# add key to database   
@app.post('/api/postkey')
def Postkey():
    try:
    # check if request other then post    
     if request.method != 'POST':
        return jsonify({'message':'such method not allowed','success':False}),404 
    #    get user data     
     data=request.json
     validate_data=api_key_schema.load(data)
    # now insert the data in mongodb 
     db=connection()
     key_col=db['keyCollection']
     key_col.insert_one(data)
     return jsonify({
        'message':'Api Key Added',
        'data':validate_data,
        'success':True
     }),200
    except ValidationError as err:
        return jsonify({
            "message": "Validation failed",
            "errors": err.messages,
            'success':False
       }) ,400
    except Exception as e:
       return jsonify({
           'message':'Internal server error',
           'error':str(e),
           'success':True
       }) ,500   
    
# collect keys from database       
@app.get('/api/getkeys')
def getKeys():
   try:
      db=connection()   
      key_col=db['keyCollection']
    #   get results
      result=key_col.find() 
      data=[]
      for doc in result:
         doc['_id']=str(doc['_id'])
         data.append(doc)

      return jsonify({'message':'Data Reterived','result':data,'success':True}),200
       
   except Exception as e:
      return jsonify({'message':'Internal Server Error','success':False}),500   

# update key   
@app.put('/api/updatekey')
def UpdateKey():
   try:
      data=request.json
    #   pass _id query in endpoint
      _id=request.args.get('_id')
      if not _id:
         return jsonify({'message': 'Missing _id in query parameters'}), 400
      if not data:
          return jsonify({'message': 'No data provided for update'}), 400   
    #   validate objectid    
      try:
            object_id = ObjectId(_id)
      except Exception:
            return jsonify({'message': 'Invalid _id format'}), 400
      # Connect to the database and collection
      db = connection()
      key_col = db['keyCollection']      
      # Perform the update
      result = key_col.update_one(
            {"_id": object_id},   
            {"$set": data}        
        )
      if result.matched_count == 0:
            return jsonify({'message': 'No document found with the given _id'}), 404  
      return jsonify({
            'message': 'Document updated successfully',
            'matched_count': result.matched_count,
            'modified_count': result.modified_count,
            'success': True
        }), 200

   except Exception as e:
      return jsonify({'message':'Internal Server Error'}),500   
   
# delete key   
@app.delete('/api/deletekey')
def deleteKey():
    try:
        _id=request.args.get('_id')
        if not _id:
            return jsonify({'message': 'Missing _id in query parameters','success': False}), 400
        #   validate objectid    
        try:
                object_id = ObjectId(_id)
        except Exception:
                return jsonify({'message': 'Invalid _id format','success': False}), 400    
        # Connect to the database and collection
        db = connection()
        key_col = db['keyCollection']      
        # perform delete operation   
        result=key_col.find_one_and_delete({'_id':object_id})
        # Check if the document was found and deleted
        if result is None:
            return jsonify({'message': 'No document found with the given _id', 'success': False}), 404
   
        # return success response    
        return jsonify({
            'messgae':'document deleted',
            'success':True
        }),200
    except Exception as e:
        return jsonify({'message':'Internal Server Error','success':False}),500    
