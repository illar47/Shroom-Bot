#class that holds items
class BagOfHoardingItem:
    def __init__(self, p_dataRow):
        self.name = p_dataRow[0]
        self.itemKey =  self.name.lower().replace(" ", "")
        self.lvl = p_dataRow[1]
        self.rarity = p_dataRow[2]
        self.itemType = p_dataRow[3]
        self.reqAttunement = bool(p_dataRow[4])
        self.isHomebrew = bool(p_dataRow[5])
        try:
            self.classes = p_dataRow[6] #TODO: logic to turn comma separated list into array of classes
        except IndexError:
            self.classes = []
        self.properties = p_dataRow[7]

        try:
            self.link = p_dataRow[8]
        except IndexError:
            self.link = ""
        self.isUsed = False

#class that holds location information
class encounterItem:
    def __init__(self, p_dataRow):
        self.name = p_dataRow[0]
        self.type = p_dataRow[1]
        self.creatures = p_dataRow[2] #TODO: check for comma delimited list (also for an empty entry)
        self.description = p_dataRow[3]

#class that holds NPC location      
class NPC:
    def __init__(self, p_dataRow):
        #honestly probably need something different than this? idk temp for now
        self.name = p_dataRow[0]
        self.species = "None"
        self.gender = "None"
        self.description = "None"