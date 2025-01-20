from marshmallow import Schema,fields,validates,ValidationError
from enum import Enum

# enums fields
class keyType(Enum):
    SPOT = "spot"
    FUTURES = "futures"

# built schema now    
class keySchema(Schema):
    api_key=fields.String(required=True,validate=lambda x:len(x)>0,error_messages={"required": "API key is required."})
    api_sec=fields.String(required=True,validate=lambda x:len(x)>0,error_messages={"required": "API secret is required."})
    type=fields.String(required=True,error_messages={"required": "Type is invalid."})

    # validate type    
    @validates('type')
    def validateType(self,key):
        if key not in [item.value for item in keyType]:
            raise ValueError('Type Is Invalid Must Be Spot Or Futures')

    # validate api key
    @validates('api_key')
    def validateapikey(self,key):
        if len(key)!=64:
            raise ValidationError("API key is Invalid.")
        
    # validate api sec
    @validates('api_sec')
    def validateapikey(self,key):
        if len(key)!=64:
            raise ValidationError("API Secret is Invalid.")    
