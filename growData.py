#! /usr/bin/env python

import os
import time
import traceback
import Adafruit_DHT
from googleapiclient.discovery import build
from google.oauth2 import service_account
from MCP3008 import MCP3008
import RPi.GPIO as GPIO

print('Waking up...')
time.sleep(15)
print('At your service, Sir.')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(16, GPIO.IN)

adc = MCP3008()

DHT_SENSOR = Adafruit_DHT.DHT22

DHT_PIN = 4

SERVICE_ACCOUNT_FILE = '/home/pi/growApp/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '1CP_OjfRSQ3IpJpMaxdXJJsvwvUsNl6iC4y8C2GxRbaE'


service = build('sheets', 'v4', credentials=credentials)

# Call the Sheets API
sheet = service.spreadsheets()

failCount = 0

with open('/home/pi/growApp/except.txt', 'a+') as excep:

    timeStamp = '----- ' + time.strftime('%m/%d') + ' at ' + time.strftime('%H:%M') + '-----'
    excep.write(timeStamp + '\n')
    excep.flush()
    
    while True:
        try:
                    
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            
            value = adc.read(channel = 0)
            
            #request1 = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
             #         range="growdata!E2", valueInputOption="USER_ENTERED", body={"values":[moistValue]}).execute()
            
            if humidity is not None and temperature is not None:
                temperature = temperature*(9/5) + 32

                temperature = round(temperature, 2)
                humidity = round(humidity, 2)

                element = [[time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity, value]]
            #data.append(element)
            #data.reverse()

                request2 = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="growdata!A2", valueInputOption="USER_ENTERED", body={"values":element}).execute()
                
            else:
                failCount = failCount + 1
                print('number of failures: ', failCount)

            if failCount >= 5:
                os.system('sudo shutdown -r now')
            
            time.sleep(900)
            
        except Exception as e:
            excep.write(str(e) + '\n')
            excep.flush()
    
