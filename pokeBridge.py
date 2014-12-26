#todo: research if pokedex flags have to be set on data write

boxLen = 1102 #size of Box in bytes
numBoxes = 14
oldBoxStarts = [0x4000, 0x4450, 0x48a0, 0x4cf0, 0x5140, 0x5590, 0x59e0, 0x6000, 0x6450, 0x68a0, 0x6cf0, 0x7140, 0x7590, 0x79e0]
#todo: different offsets for different games?
names = {1: 'Bulbasaur', 2: 'Ivysaur', 3: 'Venusaur', 4: 'Charmander', 5: 'Charmeleon', 6: 'Charizard', 7: 'Squirtle', 8: 'Wartortle', 9: 'Blastoise', 10: 'Caterpie', 11: 'Metapod', 12: 'Butterfree', 13: 'Weedle', 14: 'Kakuna', 15: 'Beedrill', 16: 'Pidgey', 17: 'Pidgeotto', 18: 'Pidgeot', 19: 'Rattata', 20: 'Raticate', 21: 'Spearow', 22: 'Fearow', 23: 'Ekans', 24: 'Arbok', 25: 'Pikachu', 26: 'Raichu', 27: 'Sandshrew', 28: 'Sandslash', 29: 'Nidoran?', 30: 'Nidorina', 31: 'Nidoqueen', 32: 'Nidoran?', 33: 'Nidorino', 34: 'Nidoking', 35: 'Clefairy', 36: 'Clefable', 37: 'Vulpix', 38: 'Ninetales', 39: 'Jigglypuff', 40: 'Wigglytuff', 41: 'Zubat', 42: 'Golbat', 43: 'Oddish', 44: 'Gloom', 45: 'Vileplume', 46: 'Paras', 47: 'Parasect', 48: 'Venonat', 49: 'Venomoth', 50: 'Diglett', 51: 'Dugtrio', 52: 'Meowth', 53: 'Persian', 54: 'Psyduck', 55: 'Golduck', 56: 'Mankey', 57: 'Primeape', 58: 'Growlithe', 59: 'Arcanine', 60: 'Poliwag', 61: 'Poliwhirl', 62: 'Poliwrath', 63: 'Abra', 64: 'Kadabra', 65: 'Alakazam', 66: 'Machop', 67: 'Machoke', 68: 'Machamp', 69: 'Bellsprout', 70: 'Weepinbell', 71: 'Victreebel', 72: 'Tentacool', 73: 'Tentacruel', 74: 'Geodude', 75: 'Graveler', 76: 'Golem', 77: 'Rapidash', 79: 'Slowpoke', 80: 'Slowbro', 81: 'Magnemite', 82: 'Magneton', 83: "Farfetch'd", 84: 'Doduo', 85: 'Dodrio', 86: 'Seel', 87: 'Dewgong', 88: 'Grimer', 89: 'Muk', 90: 'Shellder', 91: 'Cloyster', 92: 'Gastly', 93: 'Haunter', 94: 'Gengar', 95: 'Onix', 96: 'Drowzee', 97: 'Hypno', 98: 'Krabby', 99: 'Kingler', 100: 'Voltorb', 101: 'Electrode', 102: 'Exeggcute', 103: 'Exeggutor', 104: 'Cubone', 105: 'Marowak', 106: 'Hitmonlee', 107: 'Hitmonchan', 108: 'Lickitung', 109: 'Koffing', 110: 'Weezing', 111: 'Rhyhorn', 112: 'Rhydon', 113: 'Chansey', 114: 'Tangela', 115: 'Kangaskhan', 116: 'Horsea', 117: 'Seadra', 118: 'Goldeen', 119: 'Seaking', 120: 'Staryu', 121: 'Starmie', 122: 'Mr. Mime', 123: 'Scyther', 124: 'Jynx', 125: 'Electabuzz', 126: 'Magmar', 127: 'Pinsir', 128: 'Tauros', 129: 'Magikarp', 130: 'Gyarados', 131: 'Lapras', 132: 'Ditto', 133: 'Eevee', 134: 'Vaporeon', 135: 'Jolteon', 136: 'Flareon', 137: 'Porygon', 138: 'Omanyte', 139: 'Omastar', 140: 'Kabuto', 141: 'Kabutops', 142: 'Aerodactyl', 143: 'Snorlax', 144: 'Articuno', 145: 'Zapdos', 146: 'Moltres', 147: 'Dratini', 148: 'Dragonair', 149: 'Dragonite', 150: 'Mewtwo', 151: 'Mew', 152: 'Chikorita', 153: 'Bayleef', 154: 'Meganium', 155: 'Cyndaquil', 156: 'Quilava', 157: 'Typhlosion', 158: 'Totodile', 159: 'Croconaw', 160: 'Feraligatr', 161: 'Sentret', 162: 'Furret', 163: 'Hoothoot', 164: 'Noctowl', 165: 'Ledyba', 166: 'Ledian', 167: 'Spinarak', 168: 'Ariados', 169: 'Crobat', 170: 'Chinchou', 171: 'Lanturn', 172: 'Pichu', 173: 'Cleffa', 174: 'Igglybuff', 175: 'Togepi', 176: 'Togetic', 177: 'Natu', 178: 'Xatu', 179: 'Mareep', 180: 'Flaaffy', 181: 'Ampharos', 182: 'Bellossom', 183: 'Marill', 184: 'Azumarill', 185: 'Sudowoodo', 186: 'Politoed', 187: 'Hoppip', 188: 'Skiploom', 189: 'Jumpluff', 190: 'Aipom', 191: 'Sunkern', 192: 'Sunflora', 193: 'Yanma', 194: 'Wooper', 195: 'Quagsire', 196: 'Espeon', 197: 'Umbreon', 198: 'Murkrow', 199: 'Slowking', 200: 'Misdreavus', 201: 'Unown', 202: 'Wobbuffet', 203: 'Girafarig', 204: 'Pineco', 205: 'Forretress', 206: 'Dunsparce', 207: 'Gligar', 208: 'Steelix', 209: 'Snubbull', 210: 'Granbull', 211: 'Qwilfish', 212: 'Scizor', 213: 'Shuckle', 214: 'Heracross', 215: 'Sneasel', 216: 'Teddiursa', 217: 'Ursaring', 218: 'Slugma', 219: 'Magcargo', 220: 'Swinub', 221: 'Piloswine', 222: 'Corsola', 223: 'Remoraid', 224: 'Octillery', 225: 'Delibird', 226: 'Mantine', 227: 'Skarmory', 228: 'Houndour', 229: 'Houndoom', 230: 'Kingdra', 231: 'Phanpy', 232: 'Donphan', 233: 'Porygon2', 234: 'Stantler', 235: 'Smeargle', 236: 'Tyrogue', 237: 'Hitmontop', 238: 'Smoochum', 239: 'Elekid', 240: 'Magby', 241: 'Miltank', 242: 'Blissey', 243: 'Raikou', 244: 'Entei', 245: 'Suicune', 246: 'Larvitar', 247: 'Pupitar', 248: 'Tyranitar', 249: 'Lugia', 250: 'Ho-Oh', 251: 'Celebi'}
genders = {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 127, 11: 127, 12: 127, 13: 127, 14: 127, 15: 127, 16: 127, 17: 127, 18: 127, 19: 127, 20: 127, 21: 127, 22: 127, 23: 127, 24: 127, 25: 127, 26: 127, 27: 127, 28: 127, 29: 254, 30: 254, 31: 254, 32: 0, 33: 0, 34: 0, 35: 191, 36: 191, 37: 191, 38: 191, 39: 191, 40: 191, 41: 127, 42: 127, 43: 127, 44: 127, 45: 127, 46: 127, 47: 127, 48: 127, 49: 127, 50: 127, 51: 127, 52: 127, 53: 127, 54: 127, 55: 127, 56: 127, 57: 127, 58: 63, 59: 63, 60: 127, 61: 127, 62: 127, 63: 63, 64: 63, 65: 63, 66: 63, 67: 63, 68: 63, 69: 127, 70: 127, 71: 127, 72: 127, 73: 127, 74: 127, 75: 127, 76: 127, 77: 127, 78: 127, 79: 127, 80: 127, 81: 255, 82: 255, 83: 127, 84: 127, 85: 127, 86: 127, 87: 127, 88: 127, 89: 127, 90: 127, 91: 127, 92: 127, 93: 127, 94: 127, 95: 127, 96: 127, 97: 127, 98: 127, 99: 127, 100: 255, 101: 255, 102: 127, 103: 127, 104: 127, 105: 127, 106: 0, 107: 0, 108: 127, 109: 127, 110: 127, 111: 127, 112: 127, 113: 254, 114: 127, 115: 254, 116: 127, 117: 127, 118: 127, 119: 127, 120: 255, 121: 255, 122: 127, 123: 127, 124: 254, 125: 63, 126: 63, 127: 127, 128: 0, 129: 127, 130: 127, 131: 127, 132: 255, 133: 31, 134: 31, 135: 31, 136: 31, 137: 255, 138: 31, 139: 31, 140: 31, 141: 31, 142: 31, 143: 31, 144: 255, 145: 255, 146: 255, 147: 127, 148: 127, 149: 127, 150: 255, 151: 255, 152: 31, 153: 31, 154: 31, 155: 31, 156: 31, 157: 31, 158: 31, 159: 31, 160: 31, 161: 127, 162: 127, 163: 127, 164: 127, 165: 127, 166: 127, 167: 127, 168: 127, 169: 127, 170: 127, 171: 127, 172: 127, 173: 191, 174: 191, 175: 31, 176: 31, 177: 127, 178: 127, 179: 127, 180: 127, 181: 127, 182: 127, 183: 127, 184: 127, 185: 127, 186: 127, 187: 127, 188: 127, 189: 127, 190: 127, 191: 127, 192: 127, 193: 127, 194: 127, 195: 127, 196: 31, 197: 31, 198: 127, 199: 127, 200: 127, 201: 255, 202: 127, 203: 127, 204: 127, 205: 127, 206: 127, 207: 127, 208: 127, 209: 191, 210: 191, 211: 127, 212: 127, 213: 127, 214: 127, 215: 127, 216: 127, 217: 127, 218: 127, 219: 127, 220: 127, 221: 127, 222: 191, 223: 127, 224: 127, 225: 127, 226: 127, 227: 127, 228: 127, 229: 127, 230: 127, 231: 127, 232: 127, 233: 255, 234: 127, 235: 127, 236: 0, 237: 0, 238: 254, 239: 63, 240: 63, 241: 254, 242: 254, 243: 255, 244: 255, 245: 255, 246: 127, 247: 127, 248: 127, 249: 255, 250: 255, 251: 255}

#todo: remove some of these from global namespace?
GENDER_MALE = 0
GENDER_FEMALE = 254
GENDER_NONE = 255
NAME_LENGTH = 10
OT_LENGTH = 7

##Female:Male
##
##0   00 0:1 Never female
##31  1F 1:7 Rarely female
##63  3F 1:3 Sometimes female
##127 7F 1:1 Even chances
##191 BF 3:1 Usually female
##254 FE 1:0 Always female
##255 FF 0:0 No gender

class Pokemon:
    '''An individual Pokemon. Takes three bytes objects.'''
    
    def __init__(self, data, OTdata, nameData):
        from random import randint

        self.species = data[0x0]
        self.item = data[0x1] #todo: convert item IDs
        self.moves = [move for move in data[0x2:0x6]]
        self.OTID = (data[0x6] << 8) + data[0x7]
        self.exp = (data[0x8] << 16) + (data[0x9] << 8) + data[0xa]
        
        self.oldHPEV = (data[0xb] << 8) + data[0xc]
        self.oldAttackEV = (data[0xd] << 8) + data[0xe]
        self.oldDefenseEV = (data[0xf] << 8) + data[0x10]
        self.oldSpeedEV = (data[0x11] << 8) + data[0x12]
        self.oldSpecialEV = (data[0x13] << 8) + data[0x14]
        self.EVs = convertEVs([self.oldHPEV, self.oldAttackEV,
                               self.oldDefenseEV, self.oldSpeedEV,
                               self.oldSpecialEV])
        self.HPEV, self.attackEV, self.defenseEV, self.speedEV, self.spAtkEV, self.spDefEV = self.EVs
        
        self.oldAttackIV = (data[0x15] & 0xf0) >> 4
        self.oldDefenseIV = data[0x15] & 0x0f
        self.oldSpeedIV = (data[0x16] & 0xf0) >> 4
        self.oldSpecialIV = data[0x16] & 0x0f
        temp = [IV & 1 for IV in [self.oldAttackIV, self.oldDefenseIV,
                                  self.oldSpeedIV, self.oldSpecialIV]]
        self.oldHPIV = (temp[0] << 3) + (temp[1] << 2) + (temp[2] << 1) + temp[3]
        self.IVs = convertIVs([self.oldHPIV, self.oldAttackIV,
                               self.oldDefenseIV, self.oldSpeedIV,
                               self.oldSpecialIV])
        self.HPIV, self.attackIV, self.defenseIV, self.speedIV, self.spAtkIV, self.spDefIV = self.IVs
        
        PPs = data[0x17:0x1b]
        self.PPups = [(PP & 0b11000000) >> 6 for PP in PPs]
        self.PPvals = [PP & 0b00111111 for PP in PPs]
        
        self.happiness = data[0x1b]
        self.pokerus = data[0x1c] #todo: get data out of this?
        self.caught = data[0x1d:0x1f] #todo: get data out of this?
        self.level = data[0x1f]

        self.OT = oldNameTrans(OTdata)
        self.name = oldNameTrans(nameData)
        self.shiny = (self.oldDefenseIV ==
                      self.oldSpeedIV   ==
                      self.oldSpecialIV == 10) and self.oldAttackIV in [2,3,6,7,10,11,14,15]
        self.speciesName = names[self.species]

        gender = genders[self.species]
        if gender == GENDER_NONE:
            self.gender = 'genderless'
        elif gender == GENDER_MALE:
            self.gender = 'male'
        elif gender == GENDER_FEMALE:
            self.gender = 'female'
        elif self.attackIV <= (gender >> 4):
            self.gender = 'female'
        else:
            self.gender = 'male'

        self.ability = randint(0,1)

        self.game = None
        self.language = None
        self.OTGender = None
        self.personality = None
        self.secretID = None

        #todo: Unown letter

    def __str__(self):
        return "{} (Level {} {})".format(self.name, self.level, self.speciesName)

    def newPersonalityValue(self):
        '''Generates a personality value. If the Pokemon is
        shiny, a secret ID must be set.'''
        from random import randint
        
        #gender byte
        gender = self.gender
        cutoff = genders[self.species]
        if cutoff in [GENDER_NONE, GENDER_MALE, GENDER_FEMALE]:
            pg = randint(0, 255)
        else:
            if gender == 'female':
                pg = randint(0, cutoff - 1)
            else:
                pg = randint(cutoff, 255)

        p1 = randint(0, 2**16 - 1)
        p2 = (randint(0, 2**8 - 1) << 8) + pg
        
        if self.shiny:
            OTID = self.OTID
            secretID = self.secretID
            
            check = OTID ^ secretID ^ p1 ^ p2
            checkbits = list('{:0>16b}'.format(check)) #16-bit binary
            p1bits = list('{:0>16b}'.format(p1))
            for i in range(13):
                if checkbits[i] == '1':
                    p1bits[i] = '0' if p1bits[i] == '1' else '1'
            p1str = "".join(p1bits)
            p1 = eval('0b' + p1str)
            
            check = OTID ^ secretID ^ p1 ^ p2
            assert check < 8

        #todo: Unown letter

        return (p1 << 16) + p2

    def newData(self):
        '''Returns a bytes representation of the Pokemon, ready
        for writing to Generation III.'''
        from itertools import permutations

        #string lengths in bytes
        NAME_LENGTH = 10
        OT_LENGTH = 7
        languages = {'Japanese': 0x201, 'English': 0x202, 'French': 0x203, 'Italian': 0x204, 'German': 0x205, 'Korean': 0x206, 'Spanish': 0x207}
        games = {'Bonus': 0, 'Sapphire': 1, 'Ruby': 2, 'Emerald': 3, 'FireRed': 4, 'LeafGreen': 5, 'Orre': 15}

        def encrypt(sub, key):
            '''Returns an encrypted substructure (bytes object)
            using the proper 4-byte key value.'''
            
            key = makeBytes(key, 4)
            encrypted = []
            for i in range(12):
                encrypted.append(sub[i] ^ (key[i%4]))
            return bytes(encrypted)

        def makeBytes(data, size):
            '''Takes an integer, returns a little-endian bytes
            representation of the data with the given size in
            number of bytes.'''
            
            datastr = ('{:0>'+str(size*2)+'x}').format(data) #size hex bytes
            return (bytes.fromhex(datastr))[::-1]

        def makeChecksum(substructures):
            '''Takes a list of 4 substructures and returns the
            proper checksum.'''

            total = 0
            for sub in substructures:
                for i in range(0, 12, 2):
                    total += sub[i] + (sub[i+1] << 8)
            return total % (2**16)

        #create bytes for each field
        personality = makeBytes(self.personality, 4)
        OTID = makeBytes(self.OTID, 2)
        secretID = makeBytes(self.secretID, 2)
        name = newNameTrans(self.name, NAME_LENGTH)
        language = makeBytes(languages[self.language], 2)
        OT = newNameTrans(self.OT, OT_LENGTH)
        markings = makeBytes(0, 1)
        #checksum goes here
        padding = makeBytes(0, 2)

        #all substructures are created in little-endian order,
        #i.e. they're all created for direct writing (after
        #encryption that is)

        #substructure G
        species = makeBytes(self.species, 2)
        item = makeBytes(self.item, 2) #todo: translate item
        exp = makeBytes(self.exp, 4)
        #todo: make sure PPups are in the right order
        PPupsRaw = self.PPups[0] + (self.PPups[1] << 2) + (self.PPups[2] << 4) + (self.PPups[3] << 6)
        PPups = makeBytes(PPupsRaw, 1)
        happiness = makeBytes(self.happiness, 1)
        unknown = makeBytes(0, 2) #it's a mystery
        
        subG = species + item + exp + PPups + happiness + unknown

        #substructure A
        moves = [makeBytes(move, 2) for move in self.moves]
        PPvals = [makeBytes(PPval, 1) for PPval in self.PPvals]
        
        subA = moves[0] + moves[1] + moves[2] + moves[3] + PPvals[0] + PPvals[1] + PPvals[2] + PPvals[3]

        #substructure E
        HPEV, attackEV, defenseEV, speedEV, spAtkEV, spDefEV = [makeBytes(EV, 1) for EV in self.EVs]
        condition = makeBytes(0, 6)
        
        subE = HPEV + attackEV + defenseEV + speedEV + spAtkEV + spDefEV + condition

        #substructure M
        pokerus = makeBytes(self.pokerus, 1) #todo: validate this
        placeMet = makeBytes(0, 1) #todo: put actual data here

        OTGender = 1 if self.OTGender == 'female' else 0
        ball = 4 #todo: let this be customizable?
        game = games[self.game]
        levelMet = self.level #todo: make this the old met level?
        originRaw = (OTGender << 15) + (ball << 11) + (game << 7) + levelMet
        origin = makeBytes(originRaw, 2)

        ability = self.ability
        egg = 0 #don't transfer eggs, stupid
        IVs = [IV for IV in reversed(self.IVs)]
        genesRaw = (ability << 31) + (egg << 30) + (IVs[0] << 25) + (IVs[1] << 20) + (IVs[2] << 15) + (IVs[3] << 10) + (IVs[4] << 5) + IVs[5]
        genes = makeBytes(genesRaw, 4)

        ribbons = makeBytes(0, 4)

        subM = pokerus + placeMet + origin + genes + ribbons
        
        #calculate checksum
        checksumRaw = makeChecksum([subG, subA, subE, subM])
        checksum = makeBytes(checksumRaw, 2)
        
        #encrypt substructures
        key = self.personality ^ ((self.secretID << 16) + self.OTID)
        subG = encrypt(subG, key)
        subA = encrypt(subA, key)
        subE = encrypt(subE, key)
        subM = encrypt(subM, key)
        
        #determine substructure order
        order = self.personality % 24
        #todo: make the permutations table a constant?
        subs = tuple(permutations([subG, subA, subE, subM]))[order]
        
        #combine and return data
        data = bytes()
        data += personality + OTID + secretID + name + language + OT + markings + checksum + padding
        data += subs[0] + subs[1] + subs[2] + subs[3]
        return data

class Box:
    '''A sequence of Pokemon that represents a box. Takes a
    bytes object.'''

    def __init__(self, data):
        PKMN_LENGTH = 32 #size of Pokemon in bytes
        BOX_SIZE = 20 #max number of Pokemon per Box
        OT_LENGTH = NAME_LENGTH = 11 #size of names in bytes
    
        pkmnStart = BOX_SIZE + 2
        OTsStart = pkmnStart + BOX_SIZE*PKMN_LENGTH
        namesStart = OTsStart + BOX_SIZE*OT_LENGTH
        
        count = data[0x0]
        self.species = [i for i in data[0x1:0x1 + count]]
        self.pokemon = []
        #todo: make this loop look nicer by incrementing variables?
        for i in range(count):
            pkmnData = data[pkmnStart + i*PKMN_LENGTH:pkmnStart + (i+1)*PKMN_LENGTH]
            OTData = data[OTsStart + i*OT_LENGTH:OTsStart + (i+1)*OT_LENGTH]
            nameData = data[namesStart + i*NAME_LENGTH:namesStart + (i+1)*NAME_LENGTH]
            self.pokemon.append(Pokemon(pkmnData, OTData, nameData))

    def __getitem__(self, key):
        return self.pokemon[key]

    def __iter__(self):
        return iter(self.pokemon)

    def __len__(self):
        return len(self.pokemon)

def convertEVs(EVs):
    '''Takes a list of old EVs (stat exp) and returns a list of new EVs
    after converting and adjusting for EV sum limits.'''

    #convert
    #todo: change this conversion factor?
    EVs = [EV >> 8 for EV in EVs] + [EVs[4] >> 8] #spAtk == spDef == special
    #legalize
    while sum(EVs) > 510:
        for i,EV in enumerate(EVs):
            EVs[i] = EV - 1 if EV > 0 else EV
    return EVs

def convertIVs(IVs):
    '''Takes a list of old IVs and returns a list of new adjusted IVs.'''
    from random import randint

    newIVs = []
    for IV in IVs:
        bonus = randint(0,1)
        newIVs.append(IV*2 + bonus)
    bonus = randint(0,1)
    newIVs.append(IVs[4]*2 + bonus) #spAtk and spDef both based on special
    return newIVs

def oldNameTrans(data):
    '''Translates an old encoded name or OT. Takes a bytes object,
    returns a string.'''

    stop = 0x50
    table = {128: 'A', 129: 'B', 130: 'C', 131: 'D', 132: 'E', 133: 'F', 134: 'G', 135: 'H', 136: 'I', 137: 'J', 138: 'K', 139: 'L', 140: 'M', 141: 'N', 142: 'O', 143: 'P', 144: 'Q', 145: 'R', 146: 'S', 147: 'T', 148: 'U', 149: 'V', 150: 'W', 151: 'X', 152: 'Y', 153: 'Z',
             154: '(', 155: ')', 156: ':', 157: ';', 158: '[', 159: ']',
             160: 'a', 161: 'b', 162: 'c', 163: 'd', 164: 'e', 165: 'f', 166: 'g', 167: 'h', 168: 'i', 169: 'j', 170: 'k', 171: 'l', 172: 'm', 173: 'n', 174: 'o', 175: 'p', 176: 'q', 177: 'r', 178: 's', 179: 't', 180: 'u', 181: 'v', 182: 'w', 183: 'x', 184: 'y', 185: 'z',
             225: 'PK', 226: 'MN', 227: '-', 230: '?', 231: '!', 232: '.', 127: ' ', 241: '*', 243: '/', 244: ',',
             246: '0', 247: '1', 248: '2', 249: '3', 250: '4', 251: '5', 252: '6', 253: '7', 254: '8', 255: '9'}
    word = ''
    for byte in data:
        if byte == stop:
            return word
        word += table[byte]

def newNameTrans(name, length):
    '''Translates a name into a new bytes object, padding up to
    length if necessary.'''

    stop = 0xFF
    table = {' ': 0, 'PK': 83, 'MN': 84, '(': 92, ')': 93,
             '0': 161, '1': 162, '2': 163, '3': 164, '4': 165, '5': 166, '6': 167, '7': 168, '8': 169, '9': 170,
             '!': 171, '?': 172, '.': 173, '-': 174, ',': 184, '*': 185, '/': 186,
             'A': 187, 'B': 188, 'C': 189, 'D': 190, 'E': 191, 'F': 192, 'G': 193, 'H': 194, 'I': 195, 'J': 196, 'K': 197, 'L': 198, 'M': 199, 'N': 200, 'O': 201, 'P': 202, 'Q': 203, 'R': 204, 'S': 205, 'T': 206, 'U': 207, 'V': 208, 'W': 209, 'X': 210, 'Y': 211, 'Z': 212,
             'a': 213, 'b': 214, 'c': 215, 'd': 216, 'e': 217, 'f': 218, 'g': 219, 'h': 220, 'i': 221, 'j': 222, 'k': 223, 'l': 224, 'm': 225, 'n': 226, 'o': 227, 'p': 228, 'q': 229, 'r': 230, 's': 231, 't': 232, 'u': 233, 'v': 234, 'w': 235, 'x': 236, 'y': 237, 'z': 238,
             ':': 240}
    #note: ;, [, and ] are missing
    data = [table[i] for i in name]
    if len(data) < length:
        data += [stop for i in range(length - len(data))]
    #todo: pad with 0xFF and then 0x00 instead of just 0xFF
    return bytes(data)

if __name__ == '__main__':
    file = open('C:/Users/Sidnoea/Documents/Video Games/Gameboy and GBA/Pokemon Crystal/Pokemon Crystal (U) [C][!].sav','br')
    data = file.read()
    file.close()
    box1 = Box(data[oldBoxStarts[0]:oldBoxStarts[0] + boxLen])
    box2 = Box(data[oldBoxStarts[1]:oldBoxStarts[1] + boxLen])
    box3 = Box(data[oldBoxStarts[2]:oldBoxStarts[2] + boxLen])

    rat = box1[17]
    rat.OTGender = 'male'
    rat.language = 'English'
    rat.game = 'Ruby'
    rat.secretID = 12345
    rat.personality = rat.newPersonalityValue()
    newData = rat.newData()