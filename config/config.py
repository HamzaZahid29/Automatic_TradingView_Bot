import os
from dotenv import load_dotenv
load_dotenv()

class Config:

    Captcha_API = os.getenv('twocaptchaKey')
    Username = os.getenv('user')  
    password = os.getenv('passkey')
    api_key = os.getenv('Binacekeys')  
    api_sec = os.getenv('binacesecrets')  
    mongoUri = os.getenv('mongoUri')
    db_Host=os.getenv("DB_HOST")
    db_port=os.getenv("DB_PORT")

