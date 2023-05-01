# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:06:50 2023

@author: Rajat
"""

from kiteconnect import KiteConnect
from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pyotp
global driver

cwd = os.chdir(("Current Working Directory"))

def autologin():
    token_path = "api_key.txt"
    key_secret = open(token_path,'r').read().split()
    kite = KiteConnect(api_key=key_secret[0])
    service = webdriver.chrome.service.Service('./chromedriver')
    service.start()
    options = webdriver.ChromeOptions()
    #options.add_experimental_option("detach", True)
    #options = Options()
    #options.add_argument('--headless')
    options_C = options.to_capabilities()
    
    driver = webdriver.Remote(service.service_url, options_C)
    driver.get(kite.login_url())
    driver.implicitly_wait(10)
    username = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
    username.send_keys(key_secret[2])
    password = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')    
    password.send_keys(key_secret[3])
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/form/div[4]/button').click()
    authkey = pyotp.TOTP('write authenticate key here')
    #print(authkey.now())
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/input').send_keys(authkey.now())
    #driver.implicitly_wait(10)
    time.sleep(10)
    print(driver.current_url)
    request_token = driver.current_url.split('request_token=')[1].split('&action')[0]
    print(request_token)
    with open('request_token.txt', 'w') as the_file:
        the_file.write(request_token)
    driver.quit()
    
autologin() 
request_token = open("request_token.txt", 'r').read()
print(request_token)
key_secret = open("api_key.txt", 'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
data = kite.generate_session(request_token, api_secret=key_secret[1])
with open('access_token.txt', 'w') as file:
    file.write(data['access_token'])
    

