from marshmallow import Schema, fields, validates, ValidationError
from enum import Enum

# Marshmallow schema
class keySchema(Schema):
    # Define fields with validation
    api_key = fields.String(
        required=True,
        validate=lambda x: len(x) > 0,
        error_messages={"required": "API key is required."},
    )
    api_sec = fields.String(
        required=True,
        validate=lambda x: len(x) > 0,
        error_messages={"required": "API secret is required."},
    )
    type = fields.String(required=True, error_messages={"required": "Type is invalid."})
    quantity=fields.String(required=True,error_messages={"required": "qunatity is invalid."})

    # Validate 'type' field (Must be in the Enum values)
    @validates('type')
    def validate_type(self, key):
        # print("Validating type:", type(key)) 
        if key not in ['spot', 'future']:
            raise ValidationError('Type is invalid. Must be Spot or Futures.')
    # Validate 'api_key' field
    @validates('api_key')
    def validate_api_key(self, key):
        # print("Validating api_key:", key) 
        if len(key) != 64:
            raise ValidationError("API key is invalid. It must be exactly 64 characters.")

    # Validate 'api_sec' field
    @validates('api_sec')
    def validate_api_sec(self, key):
        # print("Validating api_sec:", key) 
        if len(key) != 64:
            raise ValidationError("API Secret is invalid. It must be exactly 64 characters.")
