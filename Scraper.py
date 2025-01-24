# importing packages
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tradingbinance.bi__api__ import main_api_container
from selenium_stealth import stealth
from twocaptcha import TwoCaptcha
from time import sleep
from helper.extractprice import give_me_symbol_price
import random

# intailize the class
class TradingView:
    # creating constructor
    def __init__(self,Captcha_API,Username,password):
        # ensure the required values 
        if not Captcha_API or not Username or not password:
            raise ValueError("Captcha_API, Username, and Password must be provided.")
        # class attributes    
        self.username=Username
        self.password=password
        self.options=self.chromeOptions()
        self.solver=TwoCaptcha(Captcha_API)
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

    # solving the captcha    
    def solve_captcha(self):
        try:
          result=self.solver.solve_captcha(site_key='6Lcqv24UAAAAAIvkElDvwPxD0R8scDnMpizaBcHQ',page_url='https://www.tradingview.com/')
          return result
        except Exception as e:
            print('got an exception whilen solving the captcha')    

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
                print('Login Successfull.....')
                sleep(2)
                try:
                    # genrating g-token for preventing the bot detection
                    token=self.solve_captcha()
                    # self.driver.execute_script(script,token)
                    container=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.recaptchaContainer-LQwxK8Bm')))
                    captcha_response =container.find_element(By.CSS_SELECTOR,'#g-recaptcha-response')
                    self.driver.execute_script('arguments[0].innerHTML=arguments[0]',captcha_response,token)
                    iframe=WebDriverWait(self.driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,'iframe[title="reCAPTCHA"]')))
                    print(iframe)
                    click_checkbox=self.driver.find_element(By.XPATH,'//*[@id="recaptcha-anchor"]')
                    click_checkbox.click()
                    print('sending success..')
                    self.driver.switch_to.default_content()
                    sleep(7)
                    submit_form.click()
                    sleep(4)
                except TimeoutException as e:
                    print('Got An Undected Captcha')    
            except TimeoutException as e:
                print('click by email button unable to track')    

        except Exception as e:
            print('got exception from call_enter_credentials*()',e)    

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
                # just call enter credentails method
                self.call_enter_credentials()
             except TimeoutException as e:
                print('we unable to look signin link')   
         except TimeoutException as e:
             print('sign_up_btn not found')    
        except Exception as e:
            print('got exception at Login()',e)    

    # analyzing the chart        
    def analyzeChart(self):
        try:
          alert_selctor='.itemInnerInner-JUpQSPBo'
          while True:
              try:
                  get_alerts=WebDriverWait(self.driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,alert_selctor)))
                  for get_alert in get_alerts:
                        msg=get_alert.text
                        if not msg.strip():
                            continue
                        signal=None
                        time=None
                        symbol=None
                        Price=None
                        try:
                            get_time=get_alert.find_element(By.CSS_SELECTOR,'.time-m_7l3VrU')
                            time=get_time.text
                        except TimeoutException as e:
                            print('Miss Time')    
                        try:
                            get_symbol=get_alert.find_element(By.CSS_SELECTOR,'div.text-LoO6TyUc.ellipsis-LoO6TyUc')    
                            symbol=get_symbol.text
                            print(symbol)
                        except TimeoutException as e:
                            print('Miss Symbol')    
                        if symbol:
                            try:
                             Price=give_me_symbol_price(symbol) 
                            except TimeoutException as e:
                                print('Miss Price')
                            except Exception as e:
                                print('Got An exception')        
                        

                        # handling the checkes in the code                   
                        if 'Buy Signal'.lower() in msg.lower():
                            signal='Buy'
                            print('Send Request To Binace Api For Buying')
                        elif 'Sell Signal'.lower() in msg.lower():
                            signal='Sell'
                            print('send request to Binance Api For Selling')    
                        elif 'BTP Signal'.lower() in msg.lower():
                            signal='Btp'
                            print('call btp')    
                        elif 'STP Signal'.lower() in msg.lower():
                            signal='Stp'
                            print('call stp')    
                        elif 'SSL Signal'.lower() in msg.lower():
                            signal='Ssl'
                            print('call SSL')    
                        elif 'BSL Signal'.lower() in msg.lower():
                            signal='Bsl'
                            print('call BSL')    
                        else:
                            print('invalid signal')    

                        # making json object    
                        data={
                                'type':'future',                          
                                'Price':Price,
                                'Symbol':symbol,
                                'Time':time,
                                'Signal':signal,
                                'Quantity':0.01 
                            } 

                        # pass that object to api method now    
                        if data['Price'] and data['Signal'] and data['Time'] and data['Symbol']:
                            print(data)
                            main_api_container(data)

                        try:
                            close_alert=get_alert.find_element(By.CSS_SELECTOR,'div.closeButton-ZZzgDlel')    
                            close_alert.click()
                        except TimeoutException as e:
                            print('Unable To Close It')    
                        except StaleElementReferenceException as e:
                            continue    
              except StaleElementReferenceException as e:
                        continue      
              except TimeoutException as e:
                  pass    
                  sleep(5)
        except Exception as e:
            print('got exception while analyzeChart',e)    

    # opening the chart method        
    def openChart(self):
        '''
        simple method which open the url of chart
        '''
        try:
                self.driver.get('https://www.tradingview.com/chart/vZbJVznC/?symbol=BINANCE%3AVTHOUSDT')
                sleep(1)
                # here we just calling analyze the chart
                self.analyzeChart()
        except Exception as e:
            print('Got Error while opening chart')    
            


        