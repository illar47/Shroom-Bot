#Imports
import spreadsheetparsing
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

s_loggingTag = "SHROOMBOT|XLSX-PARSER| "

#helper that parses for an Excel table and outputs it.
#TODO: python is stupid af - make sure we do type checks also maybe optimize this a smidge... it's so clunky im gonna die
def parseTable(p_service, p_sheetID, p_sheetIndex): 
    # Call the Sheets API to fetch the data
    spreadsheet = p_service.spreadsheets().get(spreadsheetId=p_sheetID).execute()
    tables = spreadsheet.get('sheets', [])

    title = tables[p_sheetIndex]['properties']['title'] #TODO: use p_sheetIndex
    grid_properties = tables[p_sheetIndex]['properties'] #TODO: use p_sheetIndex

    row_count = grid_properties.get('gridProperties', {}).get('rowCount', 0)
    column_count = grid_properties.get('gridProperties', {}).get('columnCount', 0)

    table_range = f'{title}!A1:Z{row_count}' #instead of using z maybe make a touch more dynamic for space purposes? 

     # Call the Sheets API to fetch the data
    sheet_data = p_service.spreadsheets().values().get(spreadsheetId=p_sheetID, range=table_range).execute()
    
    values = sheet_data.get('values', [])

    # Print the data
    if not values:
        print(s_loggingTag + 'No data found.')
    else:
        print(s_loggingTag + f"Data from sheet '{title}':")
        for row in values:
            print(', '.join(row))

    print("\n")

    return values #TODO: figure out type
