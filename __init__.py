from validators.keySchema.keyschema import keySchema
from config.config import Config

from Scraper import TradingView

def Bot(Captcha_API,Username,password):
    Bot = TradingView(Captcha_API,Username,password)
    Bot.Login()
    Bot.openChart()
    