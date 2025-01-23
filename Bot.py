from config.config import Config 
from __init__ import Bot

if __name__=='__main__':
    Bot(Config.Captcha_API,Config.Username,Config.password)