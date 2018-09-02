# import modules
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import matplotlib.pyplot as plt

# Settung up the google spreadsheet
JSON_FILENAME = './GdirveTestApi-00124c66d42a.json'
GSHEET_NAME = 'room_temperature'
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, scope)
client_inst = gspread.authorize(credentials) 
gsheet = client_inst.open(GSHEET_NAME).sheet1

# Get data
time = [datetime.datetime.strptime(k, "%d-%m-%Y %H:%M:%S") for k in gsheet.col_values(1)[1:]]
theta = [float(k) for k in gsheet.col_values(2)[1:]]

# plot
hf = plt.figure()
plt.plot(time, theta)
plt.ylabel('temperature (°C)', fontsize=16)
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid()
plt.show()
