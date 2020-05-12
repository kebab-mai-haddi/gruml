import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import csv
import xlrd

# use creds to create a client to interact with the Google Drive API
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)

path = 'Use_Case_test_cliDependency_2.xlsx'

# read excel file
wb = xlrd.open_workbook(path)

file_id = client.create('Use_Case_test_cliDependency_2')
print('File ID is: {}'.format(file_id.id))
print('URL is: {}'.format(file_id.url))
# content = pd.read_excel(path, header=None)
# csv_path = path.split('.xlsx')[0]+'.csv'
# content.to_csv(csv_path, index=False, header=False)
# content = open(csv_path, 'r').read()
client.import_csv(file_id.id, wb)
print('Check client')
client.insert_permission(file_id.id, None, perm_type='anyone', role='reader')
