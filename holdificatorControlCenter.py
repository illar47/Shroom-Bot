import holdificators as holder
import random

class holdificatorControlCenter:
    def __init__(self):
        self.itemTable = None #TODO: change to empty lists
        self.npcTable = None
        self.encTable = None
        self.itemHolder = {}
        self.npcHolder = {}
        self.encHolder = {}

    def testificate ():
        print("STROOB")
    
    def setTables(self, p_itemTable, p_npc_table, p_enc_table): 

        #parse each table and save as holdificator table?
        self.itemTable = p_itemTable
        self.npcTable = p_npc_table
        self.encTable = p_enc_table

        for row in p_itemTable: 
            tempItem = holder.BagOfHoardingItem(row)
            self.itemHolder[tempItem.name] = tempItem

    def findItem(self, to_find): 
        if to_find in self.itemHolder: 
            return self.itemHolder.get(to_find)
        
    def pickRandomItem(self, p_level, p_rarity, p_character):
        randKey = random.choice(list(self.itemHolder.keys()))
        return self.itemHolder[randKey]
        
    def pickRandomEncounter(self):
        randKey = random.choice(list(self.encHolder.keys()))
        return self.encHolder[randKey]
#put tables into holdificator control center
controlCenter = holdificatorControlCenter(); 