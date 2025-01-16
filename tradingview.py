# importing packages
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from time import sleep
import random

# intailize the class
class TradingView:
    # creating constructor
    def __init__(self):
        self.username='govaho920@gmail.com'
        self.password='govaho920@gmail.com'
        self.options=self.chromeOptions()
        self.driver=webdriver.Chrome(options=self.options)
        self.apply_sealth(self.driver)
    # creating the options method    
    def chromeOptions(self):
        options=webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--incognito')
        options.add_argument('--disable-extensions')
        return options
    # create the sealth method    
    def apply_sealth(self,driver):
        stealth(driver,languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)
    # function to send keys    
    def call_enter_credentials(self):
        try:
            try:
                sleep(1)
                email_btn=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[8]/div/div/div[1]/div/div[2]/div[2]/div/div/button')))
                email_btn.click()
                sleep(1)
                email_input=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'input[name="id_username"]')))
                email_input.send_keys(self.username)
                pass_input=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'input[name="id_password"]')))
                pass_input.send_keys(self.password)
                sleep(2)
                submit_form=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[8]/div/div/div[1]/div/div[2]/div[2]/div/div/div/form/button')))
                submit_form.click()
                sleep(4)
            except TimeoutException as e:
                print('click by email button unable to track')    

        except Exception as e:
            print('got exception from call_enter_credentials*()')    
            
    # now login in the account    
    def Login(self):
        try:
         self.driver.get('https://www.tradingview.com/pricing/?source=header_go_pro_button&feature=start_free_trial')
         sleep(random.uniform(2,4))
         try:
             sign_up_btn=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[3]/div[4]/div/div[2]/div/div[2]/button[1]/span')))
             sign_up_btn.click()
             sleep(1)
             try:
                sign_in=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[8]/div/div/div[1]/div/div[2]/div[3]/p/a')))
                sign_in.click()
                sleep(1)
                self.call_enter_credentials()
             except TimeoutException as e:
                print('we unable to look signin link')   
         except TimeoutException as e:
             print('sign_up_btn not found')    
        except Exception as e:
            print('got exception at Login()',e)    


        