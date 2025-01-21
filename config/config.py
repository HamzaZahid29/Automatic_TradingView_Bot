import os

class Config:
    Captcha_API=os.getenv('twocaptchaKey')
    Username=os.getenv('usename')
    password=os.getenv('password')
    api_key=os.getenv('Binacekey')
    api_sec=os.getenv('binacesecret')
    mongouri=os.getenv('mongourl')
