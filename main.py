import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime

import multiprocessing
import os.path
import bs4
import functions_framework
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from apiclient import discovery

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Yq2WQ3yS29avc-JNrX81SmR4q4tbsVmQsOgbNOYdJPg'
SAMPLE_RANGE_NAME = 'F2'

def http(request):
    main()
    return 'OK'

def main():
    sheet = getSheet()
    user = getUsername(sheet)
    url = "https://www.reddit.com/user/" + user + "/submitted/"

    #navigate to webpage
    driver = createDriver()
    tryGet(url, driver)
    
    #click 18 and over button
    driverWait(driver,'css',"button._2iLUa1DN5bY9-oFqq3UDXm:nth-child(2)")
    
    time.sleep(2)
    #scroll down to load more
    driver.execute_script("window.scrollTo(0,document.body.scrollheight)")
    

    #get reddit info
    output1=driverWait(driver,'xpathwait', "//*[@data-click-id='subreddit']")
    output2=driverWait(driver,'xpathwait',"//*[@class='_eYtD2XCVieq6emjKBH3m']")
    output3=driverWait(driver,'xpathwait',"//*[@data-testid='post_timestamp']")
   

    postOutput(sheet, output1,'B2')
    postOutput(sheet, output2,'C2')
    postOutput(sheet, output3,'D2')

    


def postOutput(sheet, output ,range):
    val = [[i.text] for i in output]
    body = {'values':val}
    sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range,
            valueInputOption="USER_ENTERED", body=body).execute()

def createDriver():
   """Creating driver."""
   options = Options()
   options.headless = True  # Change To False if you want to see Firefox Browser Again.
   path = os.getcwd()+"\zcvnzel9.default-release"
   profile = webdriver.FirefoxProfile(path)
   driver = webdriver.Firefox(profile, options=options, executable_path=GeckoDriverManager().install())
   return driver

def tryGet(urlIn, driverIn):
    success = False
    attempts = 0
    while(success == False):
      try:
         driverIn.get(urlIn)
         success = True
         return True
      except Exception as e:
         print(e)
         time.sleep(1)
         attempts += 1
         if(attempts > 100):
            return False

def driverWait(driver, findType, selector):
   """Driver Wait Settings."""
   while True:
    tries = 0
    if findType == 'xpathwait':
        try:
               driver.find_elements(By.XPATH, selector)
               return driver.find_elements(By.XPATH, selector)
               break
        except NoSuchElementException:
                if tries <=10:
                    tries=tries+1
                    driver.implicitly_wait(0.2)
                else:
                    break
    if findType == 'css':
           try:
               driver.find_element(By.CSS_SELECTOR, selector).click()
               break
           except NoSuchElementException:
               # if tries <=3:
                #    tries=tries+1
                 #   driver.implicitly_wait(0.2)
                #else:
                    break
    elif findType == 'name':
           try:
               driver.find_element(By.NAME,selector).click()
               break
           except NoSuchElementException:
               if tries <=50:
                tries=tries+1
                driver.implicitly_wait(0.2)
               else:
                   break
    elif findType == 'class':
        try:
               driver.find_element(By.CLASS_NAME,selector).click()
               break
        except NoSuchElementException:
               if tries <=50:
                tries=tries+1
                driver.implicitly_wait(0.2)
               else:
                   break


def getSheet():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    

    try:
        sfile = os.getcwd()+ '/reddit-387223-44430a05ff99.json'
        credentials = service_account.Credentials.from_service_account_file(sfile)
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        
    except HttpError as err:
        print(err)

    return sheet
    
def getUsername(sheet):
    
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return
    print(values)
    return values[0][0]



if __name__ == '__main__':
    main()

