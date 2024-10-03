#TODO: Description of ShroomBot

#Imports
import discord
import logging
import os
from dotenv import load_dotenv

import spreadsheetparsing as xslsParser
import holdificators as holder
import holdificatorControlCenter as hcc
import discordClient

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build



load_dotenv() #Load ENV

### Static Variables ###
s_botToken = os.getenv('BOT_TOKEN')
s_serviceAccountPath = os.getenv('SERVICE_ACCOUNT_INFO_PATH')
s_spreadsheetID = os.getenv('SPREADSHEET_ID')
s_scopes =['https://www.googleapis.com/auth/spreadsheets']
s_loggingTag = "SHROOMBOT"

isAlive = True

### initalize log ###
logging.basicConfig(format='%(levelname)s|%(name)s|%(message)s')
shroomLog = logging.getLogger(s_loggingTag)
shroomLog.setLevel(logging.INFO)

shroomLog.info("Shroom Is Booting Up...")

#TODO: Future - add command line arg parser to instead take in a command line provided excel file

### power on client connection to discord ###



### load in data tables from Google Drive ###
credentials = Credentials.from_service_account_file(s_serviceAccountPath, scopes=s_scopes) # Create credentials object
service = build('sheets', 'v4', credentials=credentials) # Build the Google Sheets API service


shroomLog.info("Shroom is loading in external data...")
item_table, npc_table, loc_table = xslsParser.parseTable(service, s_spreadsheetID)
hcc.controlCenter.setTables(item_table, npc_table, loc_table)

for row in item_table: 
    tempItem = holder.BagOfHoardingItem(row)
    print("Item: " + tempItem.name)


#allTheTings = holdificatorControlCenter.BagOfHoarding(item_table, npc_table, loc_table)

#start the Client
discordClient.client.run(s_botToken)

shroomLog.info("Shroom Is Going Night Night...")

