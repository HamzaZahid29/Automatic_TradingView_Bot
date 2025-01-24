import os
from dotenv import load_dotenv
load_dotenv()

class Config:

    Captcha_API = os.getenv('twocaptchaKey')
    Username = os.getenv('usernames')  
    password = os.getenv('pass')
    api_key = os.getenv('Binacekey')  
    api_sec = os.getenv('binacesecret')  
    mongoUri = os.getenv('mongoUri')
    db_Host=os.getenv("DB_HOST")
    db_port=os.getenv("DB_PORT")

