#Imports
import spreadsheetparsing
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource

s_loggingTag = "SHROOMBOT|XLSX-PARSER| "

#helper that parses for an Excel table and outputs it.
#TODO: python is stupid af - make sure we do type checks also maybe optimize this a smidge... it's so clunky im gonna die
'''
Helper function that will connect to Google drive and parse the specified excel sheet and return it as a dictionary

Args: 
    p_service:  google Sheets API Resource that utilizes methods to let the code connect to the file
    p_sheetID:  alphanumeric value that represents the google sheet to connect to
    p_sheetIndex: the google page/sheet to parse

returns dictionary of parsed table values
'''
def parseTable(p_service:Resource, p_sheetID:str): 
    # Call the Sheets API to fetch the data
    spreadsheet = p_service.spreadsheets().get(spreadsheetId=p_sheetID).execute()
    tables = spreadsheet.get('sheets', [])
    
    item_table = gitTable(p_service, tables, p_sheetID, 0)
    npc_table =  gitTable(p_service, tables, p_sheetID, 1)
    loc_table =  gitTable(p_service, tables, p_sheetID, 2)

    return item_table, npc_table, loc_table #TODO: figure out type and also reformat as dictionary

'''
Helper function that will return the collection of values for a specific index
'''
def gitTable(p_service:Resource, p_tables, p_sheetID:str, p_sheetIndex:int):

    title = p_tables[p_sheetIndex]['properties']['title']
    grid_properties = p_tables[p_sheetIndex]['properties']

    row_count = grid_properties.get('gridProperties', {}).get('rowCount', 0)
    column_count = grid_properties.get('gridProperties', {}).get('columnCount', 0)

    table_range = f'{title}!A1:I{row_count}' #TODO: instead of using static letter maybe make a touch more dynamic for space purposes? 

     # Call the Sheets API to fetch the data
    sheet_data = p_service.spreadsheets().values().get(spreadsheetId=p_sheetID, range=table_range).execute()
    
    return sheet_data.get('values', [])
