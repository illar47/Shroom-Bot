import holdificators as holder
import tableUtils as util
import random

class holdificatorControlCenter:
    def __init__(self):
        self.itemTable = None #TODO: change to empty lists
        self.npcTable = None
        self.encTable = None
        self.itemHolder = {}
        self.npcHolder = {}
        self.encHolder = {}
 
    #set up the tables and save all the data correctly
    def setTables(self, p_itemTable, p_npc_table, p_enc_table): 

        #parse each table and save as holdificator table?
        self.itemTable = p_itemTable
        self.npcTable = p_npc_table
        self.encTable = p_enc_table

        for row in p_itemTable: 
            tempItem = holder.BagOfHoardingItem(row)
            self.itemHolder[tempItem.itemKey] = tempItem
        for row in p_enc_table:
            tempEnc = holder.encounterItem(row)
            self.encHolder[tempEnc.name] = tempEnc
        for row in p_npc_table:
            tempNPC = holder.NPC(row)
            self.npcHolder[tempNPC.name] = tempNPC

### ITEM METHODS ###

    #Finds the item specified - searches the item table
    def findItem(self, to_find): 
        searchKey = to_find.lower().replace(" ", "")
        if searchKey in self.itemHolder: 
            return self.itemHolder.get(searchKey)
    
    #selects a random item using given parameters
    def pickRandomItem(self, p_level, p_rarity, p_class):
        #TODO: make logic more efficent
        currentItems = self.itemHolder #save curr table as we gonna update
        if p_level != None:
            #search for items in currOptions that match p_level
            #save them as new currOptions
            newItems = currentItems.copy()
            for item in currentItems:
                if currentItems[item].lvl !=p_level:
                    newItems.pop(item) #should remove the item from the map
            currentItems = newItems.copy()
        if p_rarity != None: 
            #search for items in currOptions that match p_rarity
            #save them as new currOptions
            newItems = currentItems.copy()
            for item in currentItems:
                if currentItems[item].rarity !=p_rarity:
                    newItems.pop(item) #should remove the item from the map
            currentItems = newItems.copy()
        if p_class != None:
            #search for items in currOptions that match p_character
            #save them as new currOptions
            newItems = currentItems.copy()
            for item in currentItems:
                if currentItems[item].classes != p_class: #TODO: actually needs to be more complex for list
                    newItems.pop(item) #should remove the item from the map
            currentItems = newItems.copy()
        #TODO: error handling for when list is empty 
        randKey = random.choice(list(currentItems.keys()))
        return currentItems[randKey]

### ENCOUNTER METHODS ###

    #selects a random encounter based on the specified type
    def pickRandomEncounter(self, p_type):
        currentEncs = self.encHolder #save curr table as we gonna update

        if p_type != None:
            newEncs = currentEncs.copy()
            for item in currentEncs:
                if currentEncs[item].type != p_type: #TODO: actually needs to be more complex for list
                    newEncs.pop(item) #should remove the item from the map
            currentEncs = newEncs.copy()

        randKey = random.choice(list(currentEncs.keys()))
        return currentEncs[randKey]
    
### NPC METHODS ###

    #generates an npc using given parameters. 
    def generateNPC(self, p_species, p_gender, p_description):
        #get NPC name
        randKey = random.choice(list(self.npcHolder.keys()))
        npc:holder.NPC = self.npcHolder[randKey]

        #configure species
        if p_species == None:
            npc.species =  random.choice(util.s_species)
        else:
            npc.species = p_species
        
        #configure gender
        if p_gender == None:
            npc.gender = random.choice(util.s_genders)
        else:
            npc.gender = p_gender
        
        #configure description
        if p_description == None:
            npc.description = random.choice(util.s_descriptiveTraits)
        else:
            npc.description = p_description

        return npc
    
#put tables into holdificator control center
controlCenter = holdificatorControlCenter(); 