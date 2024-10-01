#class that holds items
class BagOfHoardingItem:
    def __init__(self, p_dataRow):
        self.name = p_dataRow[0]
        self.lvl = p_dataRow[1]
        self.rarity = p_dataRow[2]
        self.itemType = p_dataRow[3]
        self.reqAttunement = bool(p_dataRow[4])
        self.isHomebrew = bool(p_dataRow[5])
        self.characters = [] #TODO: logic to turn comma separated list into array
        self.properties = p_dataRow[7]

        if (8 in p_dataRow):
            self.link = p_dataRow[8]
        else:
            self.link = ""
        self.isUsed = False


#class that holds location information
class locationInformation:
    def __init__(self) -> None:
        pass

#class that holds NPC location      
class NPC:
    def __init__(self) -> None:
        pass