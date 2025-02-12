#useful utils for item table
s_validLevels = {"trinket", "low", "medium", "high"}
s_validRarity = {"common", "uncommon","rare", "very rare", "legendary"} #TODO: make all of these case insensentitive
s_assocCharacters = {} #TODO

#useful utils for encounter table 
s_validEncTypes = {"non-combat", "combat"}

#useful utils for random character table
s_species = ["Dwarf", "Elf", "Halfing", "Human", "Dragonborne", "Gnome", "Goliath", "Drow", "Half Elf", "Tiefling", "Orc", "Tortle", "unknown"]
s_genders = ["male", "female", "unknown"]
s_descriptiveTraits = ["bulbous", "tall", "squat", "muscular", "sexy", "short", "rotund", "enchanting", "domineering", "edgy"]
#validation functions
def checkItemParamValidity(p_levelVal, p_rarityVal, assocCharVal):
    if p_levelVal != None and not(p_levelVal.lower() in s_validLevels):
        return False
    if p_rarityVal != None and not(p_rarityVal.lower() in s_validRarity):
        return False
    if assocCharVal != None and not(assocCharVal.lower() in s_assocCharacters):
        return False
    return True

def checkEncounterParamValidity(p_encType):
    if p_encType != None and not (p_encType.lower() in s_validEncTypes):
        return False
    return True