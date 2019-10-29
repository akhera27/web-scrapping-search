import requests
import re
import os
import getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import time

import smtplib

url = input("Enter the url to scrape:\n")
findString = input("Enter search element:\n")
freq=input("Time-gap between searches(in seconds): ")
while True:
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        sp = str(soup).lower()
    except:
        print("Error Occured!! Retrying....in{freq} seconds")
        time.sleep(freq)
        continue
    if sp.find(findString) == -1:
        print("Not Found Yet")
        time.sleep(freq)
        continue
        
    else:
        msg = f'Subject: {findString} Found, CHECK {url}'
        fromaddr = input("From email-address: ")
        password = getpass.getpass("Enter password: ")
        os.environ["PASS"]=password
        toaddrs  = [input("To email-address: ")]
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, os.environ.get("PASS"))

        print('From: ' + fromaddr)
        print('To: ' + str(toaddrs))
        print('Message: ' + msg)
        
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        break