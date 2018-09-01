# import modules
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Reading the temperature from DS18B20+
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '/sys/bus/w1/devices/28-0516723f80ff/w1_slave'

# Settung up the google spreadsheet
JSON_FILENAME = '/home/pi/mypython/pylogger/GdirveTestApi-00124c66d42a.json'
GSHEET_NAME = 'room_temperature'
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, scope)
client_inst = gspread.authorize(credentials) 
gsheet = client_inst.open(GSHEET_NAME).sheet1

# function to get the temperature
def temp_raw():
    """
    TEMP_RAW get the information of the DS18B20+ in string format
    """
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    """
    READ_TEMP extract the temperature using temp_raw().
    """
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    
    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# write temperature on google spreadsheet
var = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
theta = read_temp()
gsheet.append_row((var,theta))
