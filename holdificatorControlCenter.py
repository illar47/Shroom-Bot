import holdificators as holder

class holdificatorControlCenter:
    def __init__(self):
        self.itemTable = None #TODO: change to empty lists
        self.npcTable = None
        self.locTable = None
        self.itemHolder = {}
        self.npcHolder = {}
        self.locHolder = {}

    # def __init__(self, p_itemTable, p_npc_table, p_loc_table):
    #     self.itemTable = p_itemTable
    #     self.npcTable = p_npc_table
    #     self.locTable = p_loc_table

    def testificate ():
        print("STROOB")
    
    def setTables(self, p_itemTable, p_npc_table, p_loc_table): 

        #parse each table and save as holdificator table?
        self.itemTable = p_itemTable
        self.npcTable = p_npc_table
        self.locTable = p_loc_table

        for row in p_itemTable: 
            tempItem = holder.BagOfHoardingItem(row)
            self.itemHolder[tempItem.name] = tempItem

    def findItem(self, to_find): 
        if to_find in self.itemHolder: 
            return self.itemHolder.get(to_find)
        
    
#put tables into holdificator control center
controlCenter = holdificatorControlCenter(); 