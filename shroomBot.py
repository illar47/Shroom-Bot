#TODO: Description of ShroomBot

#Imports
import spreadsheetparsing as xslsParser
import holdificators as holder
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import os
from dotenv import load_dotenv

load_dotenv() #Load ENV

### Static Variables ###
s_botToken = os.getenv('BOT_TOKEN')
s_serviceAccountPath = os.getenv('SERVICE_ACCOUNT_INFO_PATH')
s_spreadsheetID = os.getenv('SPREADSHEET_ID')
s_scopes =['https://www.googleapis.com/auth/spreadsheets']
s_loggingTag = "SHROOMBOT| "

print(s_loggingTag + "Shroom Is Booting Up...")

isAlive = True

### load in data tables from Google Drive ###
credentials = Credentials.from_service_account_file(s_serviceAccountPath, scopes=s_scopes) # Create credentials object
service = build('sheets', 'v4', credentials=credentials) # Build the Google Sheets API service

# item_table = xslsParser.npc_table 0)
# npc_table = xslsParser.parseTable(service, s_spreadsheetID, 1)
# loc_table = xslsParser.parseTable(service, s_spreadsheetID, 2)
print(s_loggingTag + "Shroom is loading in external data...")
item_table, npc_table, loc_table = xslsParser.parseTable(service, s_spreadsheetID)

for row in item_table: 
    tempItem = holder.BagOfHoardingItem(row)
    print("we test: " + tempItem.name)

#Accept input

#determine if user is attempting to find a random location, item, or NPC

    #if looking for item:

        #determine identifying information: i.e. level, type (weapon, equipable etc), player tags (who it would suit)

        #output random item that meets the criteria

    #if looking for location

        #determine if specific biome necessary (cave, beach, etc.)

        #output random location that meets the criteria. 

    #if looking for NPC
        #determine identifying information: gender, age, career, etc. 

        #randomly select name from list

        #randomly select remaining information that was not specified by user (gender, age, career etc)

        #maybe bug AI to quickly generate a 2 - 3 sentence character description? 
        
        #output results. 

print(s_loggingTag + "Shroom Is Going Night Night...")