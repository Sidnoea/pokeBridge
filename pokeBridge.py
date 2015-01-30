'''
This file contains all of the code necessary for transferring Pokemon
from one generation to the next. The transfer() function will do all
of the work needed; everything else is for internal use.
'''

#todo: Set Pokedex flags on transfer
#todo: Hidden Power? Probably not...
#todo: Test a bunch of Unown and shiny Unown
#todo: Documentation (usage, conversion factors, etc.)
#todo: GUI
#todo: Allow or disallow renaming of invalidly-named traded Pokemon?

class Pokemon:
    '''An individual Pokemon. Takes three bytes objects from Generation II
    and a boolean.'''

    OLD_LENGTH = 32 #length of old Pokemon in bytes
    NEW_LENGTH = 80 #length of new Pokemon in bytes
    OLD_NAME_LENGTH = 11 #length of old nickname in bytes (includes stop)
    NEW_NAME_LENGTH = 10 #length of new nickname in bytes (there is no extra)
    OLD_OT_LENGTH = 11 #length of old OT name in bytes (includes stop)
    NEW_OT_LENGTH = 7 #length of new OT name in bytes (there is no extra)
    #special gender cutoff values
    GENDER_MALE = 0
    GENDER_FEMALE = 254
    GENDER_NONE = 255
    
    def __init__(self, data, OTData, nameData, egg):
        from random import randint

        #todo: will moving these somewhere else improve efficiency?
        names = {1: 'Bulbasaur', 2: 'Ivysaur', 3: 'Venusaur', 4: 'Charmander', 5: 'Charmeleon', 6: 'Charizard', 7: 'Squirtle', 8: 'Wartortle', 9: 'Blastoise', 10: 'Caterpie', 11: 'Metapod', 12: 'Butterfree', 13: 'Weedle', 14: 'Kakuna', 15: 'Beedrill', 16: 'Pidgey', 17: 'Pidgeotto', 18: 'Pidgeot', 19: 'Rattata', 20: 'Raticate', 21: 'Spearow', 22: 'Fearow', 23: 'Ekans', 24: 'Arbok', 25: 'Pikachu', 26: 'Raichu', 27: 'Sandshrew', 28: 'Sandslash', 29: 'Nidoran?', 30: 'Nidorina', 31: 'Nidoqueen', 32: 'Nidoran?', 33: 'Nidorino', 34: 'Nidoking', 35: 'Clefairy', 36: 'Clefable', 37: 'Vulpix', 38: 'Ninetales', 39: 'Jigglypuff', 40: 'Wigglytuff', 41: 'Zubat', 42: 'Golbat', 43: 'Oddish', 44: 'Gloom', 45: 'Vileplume', 46: 'Paras', 47: 'Parasect', 48: 'Venonat', 49: 'Venomoth', 50: 'Diglett', 51: 'Dugtrio', 52: 'Meowth', 53: 'Persian', 54: 'Psyduck', 55: 'Golduck', 56: 'Mankey', 57: 'Primeape', 58: 'Growlithe', 59: 'Arcanine', 60: 'Poliwag', 61: 'Poliwhirl', 62: 'Poliwrath', 63: 'Abra', 64: 'Kadabra', 65: 'Alakazam', 66: 'Machop', 67: 'Machoke', 68: 'Machamp', 69: 'Bellsprout', 70: 'Weepinbell', 71: 'Victreebel', 72: 'Tentacool', 73: 'Tentacruel', 74: 'Geodude', 75: 'Graveler', 76: 'Golem', 77: 'Rapidash', 79: 'Slowpoke', 80: 'Slowbro', 81: 'Magnemite', 82: 'Magneton', 83: "Farfetch'd", 84: 'Doduo', 85: 'Dodrio', 86: 'Seel', 87: 'Dewgong', 88: 'Grimer', 89: 'Muk', 90: 'Shellder', 91: 'Cloyster', 92: 'Gastly', 93: 'Haunter', 94: 'Gengar', 95: 'Onix', 96: 'Drowzee', 97: 'Hypno', 98: 'Krabby', 99: 'Kingler', 100: 'Voltorb', 101: 'Electrode', 102: 'Exeggcute', 103: 'Exeggutor', 104: 'Cubone', 105: 'Marowak', 106: 'Hitmonlee', 107: 'Hitmonchan', 108: 'Lickitung', 109: 'Koffing', 110: 'Weezing', 111: 'Rhyhorn', 112: 'Rhydon', 113: 'Chansey', 114: 'Tangela', 115: 'Kangaskhan', 116: 'Horsea', 117: 'Seadra', 118: 'Goldeen', 119: 'Seaking', 120: 'Staryu', 121: 'Starmie', 122: 'Mr. Mime', 123: 'Scyther', 124: 'Jynx', 125: 'Electabuzz', 126: 'Magmar', 127: 'Pinsir', 128: 'Tauros', 129: 'Magikarp', 130: 'Gyarados', 131: 'Lapras', 132: 'Ditto', 133: 'Eevee', 134: 'Vaporeon', 135: 'Jolteon', 136: 'Flareon', 137: 'Porygon', 138: 'Omanyte', 139: 'Omastar', 140: 'Kabuto', 141: 'Kabutops', 142: 'Aerodactyl', 143: 'Snorlax', 144: 'Articuno', 145: 'Zapdos', 146: 'Moltres', 147: 'Dratini', 148: 'Dragonair', 149: 'Dragonite', 150: 'Mewtwo', 151: 'Mew', 152: 'Chikorita', 153: 'Bayleef', 154: 'Meganium', 155: 'Cyndaquil', 156: 'Quilava', 157: 'Typhlosion', 158: 'Totodile', 159: 'Croconaw', 160: 'Feraligatr', 161: 'Sentret', 162: 'Furret', 163: 'Hoothoot', 164: 'Noctowl', 165: 'Ledyba', 166: 'Ledian', 167: 'Spinarak', 168: 'Ariados', 169: 'Crobat', 170: 'Chinchou', 171: 'Lanturn', 172: 'Pichu', 173: 'Cleffa', 174: 'Igglybuff', 175: 'Togepi', 176: 'Togetic', 177: 'Natu', 178: 'Xatu', 179: 'Mareep', 180: 'Flaaffy', 181: 'Ampharos', 182: 'Bellossom', 183: 'Marill', 184: 'Azumarill', 185: 'Sudowoodo', 186: 'Politoed', 187: 'Hoppip', 188: 'Skiploom', 189: 'Jumpluff', 190: 'Aipom', 191: 'Sunkern', 192: 'Sunflora', 193: 'Yanma', 194: 'Wooper', 195: 'Quagsire', 196: 'Espeon', 197: 'Umbreon', 198: 'Murkrow', 199: 'Slowking', 200: 'Misdreavus', 201: 'Unown', 202: 'Wobbuffet', 203: 'Girafarig', 204: 'Pineco', 205: 'Forretress', 206: 'Dunsparce', 207: 'Gligar', 208: 'Steelix', 209: 'Snubbull', 210: 'Granbull', 211: 'Qwilfish', 212: 'Scizor', 213: 'Shuckle', 214: 'Heracross', 215: 'Sneasel', 216: 'Teddiursa', 217: 'Ursaring', 218: 'Slugma', 219: 'Magcargo', 220: 'Swinub', 221: 'Piloswine', 222: 'Corsola', 223: 'Remoraid', 224: 'Octillery', 225: 'Delibird', 226: 'Mantine', 227: 'Skarmory', 228: 'Houndour', 229: 'Houndoom', 230: 'Kingdra', 231: 'Phanpy', 232: 'Donphan', 233: 'Porygon2', 234: 'Stantler', 235: 'Smeargle', 236: 'Tyrogue', 237: 'Hitmontop', 238: 'Smoochum', 239: 'Elekid', 240: 'Magby', 241: 'Miltank', 242: 'Blissey', 243: 'Raikou', 244: 'Entei', 245: 'Suicune', 246: 'Larvitar', 247: 'Pupitar', 248: 'Tyranitar', 249: 'Lugia', 250: 'Ho-Oh', 251: 'Celebi'}
        genders = {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 127, 11: 127, 12: 127, 13: 127, 14: 127, 15: 127, 16: 127, 17: 127, 18: 127, 19: 127, 20: 127, 21: 127, 22: 127, 23: 127, 24: 127, 25: 127, 26: 127, 27: 127, 28: 127, 29: 254, 30: 254, 31: 254, 32: 0, 33: 0, 34: 0, 35: 191, 36: 191, 37: 191, 38: 191, 39: 191, 40: 191, 41: 127, 42: 127, 43: 127, 44: 127, 45: 127, 46: 127, 47: 127, 48: 127, 49: 127, 50: 127, 51: 127, 52: 127, 53: 127, 54: 127, 55: 127, 56: 127, 57: 127, 58: 63, 59: 63, 60: 127, 61: 127, 62: 127, 63: 63, 64: 63, 65: 63, 66: 63, 67: 63, 68: 63, 69: 127, 70: 127, 71: 127, 72: 127, 73: 127, 74: 127, 75: 127, 76: 127, 77: 127, 78: 127, 79: 127, 80: 127, 81: 255, 82: 255, 83: 127, 84: 127, 85: 127, 86: 127, 87: 127, 88: 127, 89: 127, 90: 127, 91: 127, 92: 127, 93: 127, 94: 127, 95: 127, 96: 127, 97: 127, 98: 127, 99: 127, 100: 255, 101: 255, 102: 127, 103: 127, 104: 127, 105: 127, 106: 0, 107: 0, 108: 127, 109: 127, 110: 127, 111: 127, 112: 127, 113: 254, 114: 127, 115: 254, 116: 127, 117: 127, 118: 127, 119: 127, 120: 255, 121: 255, 122: 127, 123: 127, 124: 254, 125: 63, 126: 63, 127: 127, 128: 0, 129: 127, 130: 127, 131: 127, 132: 255, 133: 31, 134: 31, 135: 31, 136: 31, 137: 255, 138: 31, 139: 31, 140: 31, 141: 31, 142: 31, 143: 31, 144: 255, 145: 255, 146: 255, 147: 127, 148: 127, 149: 127, 150: 255, 151: 255, 152: 31, 153: 31, 154: 31, 155: 31, 156: 31, 157: 31, 158: 31, 159: 31, 160: 31, 161: 127, 162: 127, 163: 127, 164: 127, 165: 127, 166: 127, 167: 127, 168: 127, 169: 127, 170: 127, 171: 127, 172: 127, 173: 191, 174: 191, 175: 31, 176: 31, 177: 127, 178: 127, 179: 127, 180: 127, 181: 127, 182: 127, 183: 127, 184: 127, 185: 127, 186: 127, 187: 127, 188: 127, 189: 127, 190: 127, 191: 127, 192: 127, 193: 127, 194: 127, 195: 127, 196: 31, 197: 31, 198: 127, 199: 127, 200: 127, 201: 255, 202: 127, 203: 127, 204: 127, 205: 127, 206: 127, 207: 127, 208: 127, 209: 191, 210: 191, 211: 127, 212: 127, 213: 127, 214: 127, 215: 127, 216: 127, 217: 127, 218: 127, 219: 127, 220: 127, 221: 127, 222: 191, 223: 127, 224: 127, 225: 127, 226: 127, 227: 127, 228: 127, 229: 127, 230: 127, 231: 127, 232: 127, 233: 255, 234: 127, 235: 127, 236: 0, 237: 0, 238: 254, 239: 63, 240: 63, 241: 254, 242: 254, 243: 255, 244: 255, 245: 255, 246: 127, 247: 127, 248: 127, 249: 255, 250: 255, 251: 255}
        items = {0: 0, 1: 1, 2: 2, 3: 179, 4: 3, 5: 4, 8: 94, 9: 14, 10: 15, 11: 16, 12: 17, 13: 18, 14: 19, 15: 20, 16: 21, 17: 22, 18: 13, 19: 85, 20: 86, 21: 37, 22: 95, 23: 96, 24: 97, 26: 63, 27: 64, 28: 65, 29: 66, 30: 222, 31: 67, 32: 68, 33: 78, 34: 98, 35: 223, 36: 110, 37: 80, 38: 23, 39: 24, 40: 25, 41: 73, 42: 83, 43: 84, 44: 74, 46: 26, 47: 27, 48: 28, 49: 75, 51: 76, 52: 77, 53: 79, 57: 182, 62: 69, 63: 34, 64: 35, 65: 36, 72: 29, 73: 183, 74: 135, 76: 203, 77: 210, 78: 133, 79: 137, 80: 136, 81: 211, 82: 187, 83: 140, 84: 134, 86: 103, 87: 104, 88: 188, 91: 189, 94: 190, 95: 209, 96: 214, 98: 207, 102: 206, 104: 217, 105: 225, 106: 194, 107: 212, 108: 208, 109: 141, 110: 106, 111: 107, 112: 195, 113: 213, 114: 13, 117: 205, 118: 224, 119: 196, 121: 30, 122: 31, 123: 32, 124: 33, 125: 204, 126: 197, 131: 108, 132: 109, 138: 215, 140: 198, 143: 199, 144: 216, 146: 200, 150: 138, 151: 201, 156: 45, 157: 4, 159: 8, 160: 7, 161: 4, 163: 202, 164: 11, 165: 4, 166: 4, 169: 93, 170: 217, 172: 218, 173: 139, 174: 142, 196: 293, 197: 294, 201: 298, 202: 299, 205: 302, 206: 303, 208: 305, 209: 306, 210: 307, 212: 309, 213: 310, 214: 311, 216: 313, 217: 314, 218: 315, 219: 316, 221: 317, 222: 318, 224: 320, 228: 324, 229: 325, 230: 326, 236: 332, 237: 333, 238: 334, 239: 335}
        #todo: test more items

        def convertEVs(EVs):
            '''Takes a list of old EVs (stat exp), returns a list of new EVs
            after converting and adjusting for EV sum limits.'''
            from math import sqrt

            #convert
            EVs = [int(sqrt(EV)) for EV in EVs + [EVs[4]]] #spAtk == spDef == special
            #legalize
            while sum(EVs) > 510:
                for i,EV in enumerate(EVs):
                    EVs[i] = EV - 1 if EV > 0 else EV
            return EVs

        def convertIVs(IVs):
            '''Takes a list of old IVs, returns a list of new adjusted IVs.'''
            from random import randint

            newIVs = []
            for IV in IVs + [IVs[4]]: #spAtk and spDef both based on special
                newIVs.append(IV*2 + randint(0,1))
            return newIVs

        self.species = data[0x0]
        self.item = items.get(data[0x1], 0) #bad items are destroyed
        self.moves = [move for move in data[0x2:0x6]]
        self.OTID = int.from_bytes(data[0x6:0x8], 'big')
        self.exp = int.from_bytes(data[0x8:0xb], 'big')
        
        self.oldHPEV = int.from_bytes(data[0xb:0xd], 'big')
        self.oldAttackEV = int.from_bytes(data[0xd:0xf], 'big')
        self.oldDefenseEV = int.from_bytes(data[0xf:0x11], 'big')
        self.oldSpeedEV = int.from_bytes(data[0x11:0x13], 'big')
        self.oldSpecialEV = int.from_bytes(data[0x13:0x15], 'big')
        self.EVs = convertEVs([self.oldHPEV,
                               self.oldAttackEV,
                               self.oldDefenseEV,
                               self.oldSpeedEV,
                               self.oldSpecialEV])
        self.HPEV, self.attackEV, self.defenseEV, self.speedEV, self.spAtkEV, self.spDefEV = self.EVs
        
        self.oldAttackIV = data[0x15] >> 4
        self.oldDefenseIV = data[0x15] & 0x0f
        self.oldSpeedIV = data[0x16] >> 4
        self.oldSpecialIV = data[0x16] & 0x0f
        temp = [IV & 1 for IV in [self.oldAttackIV,
                                  self.oldDefenseIV,
                                  self.oldSpeedIV,
                                  self.oldSpecialIV]]
        self.oldHPIV = (temp[0] << 3) + (temp[1] << 2) + (temp[2] << 1) + temp[3]
        self.IVs = convertIVs([self.oldHPIV,
                               self.oldAttackIV,
                               self.oldDefenseIV,
                               self.oldSpeedIV,
                               self.oldSpecialIV])
        self.HPIV, self.attackIV, self.defenseIV, self.speedIV, self.spAtkIV, self.spDefIV = self.IVs
        
        PPs = data[0x17:0x1b]
        self.PPups = [(PP & 0b11000000) >> 6 for PP in PPs]
        self.PPvals = [PP & 0b00111111 for PP in PPs]
        
        self.happiness = data[0x1b]
        self.pokerus = data[0x1c]
        self.caught = data[0x1d:0x1f] #todo: get data out of this?
        self.level = data[0x1f]

        self.OT = oldNameTrans(OTData)
        self.name = oldNameTrans(nameData)
        self.egg = egg
        
        self.shiny = (self.oldDefenseIV ==
                      self.oldSpeedIV   ==
                      self.oldSpecialIV == 10) and self.oldAttackIV in [2,3,6,7,10,11,14,15]
        self.speciesName = names[self.species]

        self.genderCutoff = genders[self.species]
        if self.genderCutoff == self.GENDER_NONE:
            self.gender = 'genderless'
        elif self.genderCutoff == self.GENDER_MALE:
            self.gender = 'male'
        elif self.genderCutoff == self.GENDER_FEMALE:
            self.gender = 'female'
        elif self.attackIV <= (self.genderCutoff >> 4):
            self.gender = 'female'
        else:
            self.gender = 'male'

        if self.species == 201: #Unown         
            b1 = (self.oldAttackIV  & 0b0110) >> 1
            b2 = (self.oldDefenseIV & 0b0110) >> 1
            b3 = (self.oldSpeedIV   & 0b0110) >> 1
            b4 = (self.oldSpecialIV & 0b0110) >> 1
            index = (b1 << 6) + (b2 << 4) + (b3 << 2) + b4
            index = int(index/10)
            self.letter = chr(index + ord('a')) #a = 0, b = 1...
        else:
            self.letter = None

        self.ability = None
        self.game = None
        self.language = None
        self.OTGender = None
        self.personality = None
        self.secretID = None

    def __str__(self):
        return "{} (Level {} {})".format(self.name, self.level, self.speciesName)

    def setAbility(self):
        '''Sets an ability for the Pokemon. A personality value must be
        set first.'''

        #list of Pokemon species with two abilities
        doubleAbilities = (19, 20, 23, 24, 50, 51, 54, 55, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 88, 89, 95, 98, 99, 100, 101, 104, 105, 108, 111, 112, 113, 118, 119, 120, 121, 131, 138, 139, 140, 141, 142, 143, 161, 162, 163, 164, 165, 166, 167, 168, 170, 171, 175, 176, 177, 178, 183, 184, 185, 186, 190, 193, 194, 195, 199, 203, 206, 207, 208, 209, 211, 214, 215, 218, 219, 222, 225, 226, 227, 228, 229, 242)
        abilityBit = self.personality % 2
        if abilityBit == 1 and self.species in doubleAbilities:
            self.ability = 1
        else:
            self.ability = 0

    def setPersonality(self):
        '''Sets a personality value for the Pokemon. A secret ID must be set
        first.'''
        from random import randint

        OTID = self.OTID
        secretID = self.secretID
        
        #gender byte
        cutoff = self.genderCutoff
        if cutoff in [self.GENDER_NONE, self.GENDER_MALE, self.GENDER_FEMALE]:
            pg = randint(0, 255)
        else:
            if self.gender == 'female':
                pg = randint(0, cutoff - 1)
            else:
                pg = randint(cutoff, 255)

        p1 = randint(0, 2**16 - 1) #upper half of personality
        p2 = (randint(0, 2**8 - 1) << 8) + pg #lower half
        
        if self.shiny:
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

        if self.species == 201: #Unown
            uNumber = ord(self.letter) - ord('a') #a = 0, b = 1...
            for i in range(uNumber, 2**8, 28): #26 letters + 2 punctuation
                u1 = (i & 0b11000000) >> 6
                u2 = (i & 0b00110000) >> 4
                u3 = (i & 0b00001100) >> 2
                u4 = (i & 0b00000011)
                newp1 = (p1 & 0b1111110011111100) + (u1 << 8) + u2
                newp2 = (p2 & 0b1111110011111100) + (u3 << 8) + u4

                if self.shiny:
                    check = OTID ^ secretID ^ newp1 ^ newp2
                    if check < 8:
                        break
                else:
                    break
            #temp
            else:
                raise Exception('Could not give a proper PV to ' + str(self))
            p1, p2 = newp1, newp2

        check = OTID ^ secretID ^ p1 ^ p2
        if not self.shiny and check < 8:
            print('Whoops! Made {} shiny.'.format(self)) #temp
            return self.setPersonality()

        self.personality = (p1 << 16) + p2

    def newData(self):
        '''Returns a bytes representation of the Pokemon, ready
        for writing to Generation III.'''

        languages = {'Japanese': 0x201,
                     'English' : 0x202,
                     'French'  : 0x203,
                     'Italian' : 0x204,
                     'German'  : 0x205,
                     'Korean'  : 0x206,
                     'Spanish' : 0x207}
        games = {'Bonus'    : 0,
                 'Sapphire' : 1,
                 'Ruby'     : 2,
                 'Emerald'  : 3,
                 'FireRed'  : 4,
                 'LeafGreen': 5,
                 'Orre'     : 15}
        #substructure orders
        orders = (('g', 'a', 'e', 'm'), ('g', 'a', 'm', 'e'), ('g', 'e', 'a', 'm'), ('g', 'e', 'm', 'a'), ('g', 'm', 'a', 'e'), ('g', 'm', 'e', 'a'), ('a', 'g', 'e', 'm'), ('a', 'g', 'm', 'e'), ('a', 'e', 'g', 'm'), ('a', 'e', 'm', 'g'), ('a', 'm', 'g', 'e'), ('a', 'm', 'e', 'g'), ('e', 'g', 'a', 'm'), ('e', 'g', 'm', 'a'), ('e', 'a', 'g', 'm'), ('e', 'a', 'm', 'g'), ('e', 'm', 'g', 'a'), ('e', 'm', 'a', 'g'), ('m', 'g', 'a', 'e'), ('m', 'g', 'e', 'a'), ('m', 'a', 'g', 'e'), ('m', 'a', 'e', 'g'), ('m', 'e', 'g', 'a'), ('m', 'e', 'a', 'g'))

        def encrypt(sub, key):
            '''Returns an encrypted substructure (bytes object)
            using the proper 4-byte key value.'''
            
            key = key.to_bytes(4, 'little')
            encrypted = []
            for i,byte in enumerate(sub):
                encrypted.append(byte ^ key[i%4])
            return bytes(encrypted)

        def makeChecksum(substructures):
            '''Takes a list of unencrypted substructures, returns the
            proper checksum.'''

            total = 0
            for sub in substructures:
                for i in range(0, len(sub), 2):
                    total += int.from_bytes(sub[i:i+2], 'little')
            return total % (2**16)

        #create bytes for each field
        personality = self.personality.to_bytes(4, 'little')
        OTID = self.OTID.to_bytes(2, 'little')
        secretID = self.secretID.to_bytes(2, 'little')
        name = newNameTrans(self.name, self.NEW_NAME_LENGTH)
        language = languages[self.language].to_bytes(2, 'little')
        OT = newNameTrans(self.OT, self.NEW_OT_LENGTH)
        markings = bytes(1) #no markings
        #checksum goes here
        padding = bytes(2)

        #substructure G
        species = self.species.to_bytes(2, 'little')
        item = self.item.to_bytes(2, 'little')
        exp = self.exp.to_bytes(4, 'little')
        PPupsRaw = self.PPups[0] + (self.PPups[1] << 2) + (self.PPups[2] << 4) + (self.PPups[3] << 6)
        PPups = PPupsRaw.to_bytes(1, 'little')
        happiness = self.happiness.to_bytes(1, 'little')
        unknown = bytes(2) #it's a mystery
        
        subG = species + item + exp + PPups + happiness + unknown

        #substructure A
        moves = [move.to_bytes(2, 'little') for move in self.moves]
        PPvals = [PPval.to_bytes(1, 'little') for PPval in self.PPvals]
        
        subA = moves[0] + moves[1] + moves[2] + moves[3] + PPvals[0] + PPvals[1] + PPvals[2] + PPvals[3]

        #substructure E
        EVs = [EV.to_bytes(1, 'little') for EV in self.EVs]
        HPEV, attackEV, defenseEV, speedEV, spAtkEV, spDefEV = EVs
        condition = bytes(6) #no condition
        
        subE = HPEV + attackEV + defenseEV + speedEV + spAtkEV + spDefEV + condition

        #substructure M
        pokerus = self.pokerus.to_bytes(1, 'little')
        placeMet = int.to_bytes(254, 1, 'little') #todo: put actual data here

        OTGender = 1 if self.OTGender == 'female' else 0
        ball = 4 #todo: let this be customizable? (not for eggs)
        game = games[self.game]
        levelMet = self.level #todo: make this the old met level?
        originRaw = (OTGender << 15) + (ball << 11) + (game << 7) + levelMet
        origin = originRaw.to_bytes(2, 'little')

        ability = self.ability
        egg = self.egg
        IVs = [IV for IV in reversed(self.IVs)]
        genesRaw = (ability << 31) + (egg << 30) + (IVs[0] << 25) + (IVs[1] << 20) + (IVs[2] << 15) + (IVs[3] << 10) + (IVs[4] << 5) + IVs[5]
        genes = genesRaw.to_bytes(4, 'little')

        ribbons = bytes(4) #no ribbons

        subM = pokerus + placeMet + origin + genes + ribbons
        
        #calculate checksum
        checksumRaw = makeChecksum([subG, subA, subE, subM])
        checksum = checksumRaw.to_bytes(2, 'little')
        
        #encrypt substructures
        key = self.personality ^ ((self.secretID << 16) + self.OTID)
        subG = encrypt(subG, key)
        subA = encrypt(subA, key)
        subE = encrypt(subE, key)
        subM = encrypt(subM, key)
        
        #determine substructure order
        d = {'g': subG, 'a': subA, 'e': subE, 'm': subM}
        order = orders[self.personality % 24]
        subs = [d[i] for i in order]
        
        #combine and return data
        data = bytes()
        data += personality + OTID + secretID + name + language + OT + markings + checksum + padding
        data += subs[0] + subs[1] + subs[2] + subs[3]
        return data

class Box:
    '''A sequence of Pokemon that represents a box. Takes a bytes object
    from Generation II.'''

    OLD_SIZE = 20 #max number of Pokemon per old Box
    NEW_SIZE = 30 #max number of Pokemon per new Box
    OLD_LENGTH = 1104 #length of old Box in bytes
    NEW_LENGTH = NEW_SIZE*Pokemon.NEW_LENGTH #length of new Box in bytes

    def __init__(self, data):
        pkmnLen = Pokemon.OLD_LENGTH
        boxSize = self.OLD_SIZE
        nameLen = Pokemon.OLD_NAME_LENGTH
        OTLen = Pokemon.OLD_OT_LENGTH
        eggID = 0xFD #species number for eggs

        count = data[0x0]
        species = [i for i in data[0x1:0x1 + count]]
        self.pokemon = []

        #todo: maybe just put the literals here?
        curPkmn = boxSize + 2
        curOT = curPkmn + boxSize*pkmnLen
        curName = curOT + boxSize*OTLen
        for i in range(count):
            pkmnData = data[curPkmn:curPkmn + pkmnLen]
            OTData = data[curOT:curOT + OTLen]
            nameData = data[curName:curName + nameLen]
            egg = species[i] == eggID
            
            self.pokemon.append(Pokemon(pkmnData, OTData, nameData, egg))
            
            curPkmn += pkmnLen
            curOT += OTLen
            curName += nameLen

    def __getitem__(self, key):
        return self.pokemon[key]

    def __iter__(self):
        return iter(self.pokemon)

    def __len__(self):
        return len(self.pokemon)

    def __str__(self):
        return '\n'.join([p.__str__() for p in self])

    def newData(self):
        '''Returns a bytes representation of the Box, ready for writing to
        Generation III.'''

        pkmnLen = Pokemon.NEW_LENGTH
        boxSize = self.NEW_SIZE

        data = bytes()
        for p in self:
            data += p.newData()
        data += bytes(pkmnLen*(boxSize-len(self))) #empty slots
        return data

    def setTraits(self, game, language, OTGender, secretID):
        '''Sets all of the parameters as traits for every Pokemon in the
        Box, then gives each Pokemon a personality value and ability.'''

        for p in self:
            p.game = game
            p.language = language
            p.OTGender = OTGender
            p.secretID = secretID
            p.setPersonality()
            p.setAbility()

class Sector:
    '''A 4KB section of a Generation III save game. Takes an integer ID and
    save index.'''

    LENGTH = 4096 #final length in bytes
    VALIDATED_BOX_LENGTH = 3968 #length of validated data in "Box Sector" in bytes
    FIRST_BOX_ID = 5 #ID of Sector with Box 1 data
    FIRST_BOX_OFFSET = 4 #offset of data for Box 1 within its Sector
    LAST_BOX_ID = 13 #ID of Sector with Box 14 data
    
    def __init__(self, ID, saveIndex):
        #lengths of checksum-validated regions in bytes
        lengths = {0: 3884, 1: 3968, 2: 3968, 3: 3968, 4: 3848,
                   5: 3968, 6: 3968, 7: 3968, 8: 3968, 9: 3968,
                   10: 3968, 11: 3968, 12: 3968, 13: 2000}
        
        self.ID = ID
        self.saveIndex = saveIndex
        self.maxLength = lengths[ID]
        self.data = bytes()

    def makeChecksum(self):
        '''Returns a proper checksum for the Sector.'''

        checksum = 0
        for i in range(0, self.maxLength, 4):
            checksum += int.from_bytes(self.data[i:i+4], 'little')
        checksum = (checksum % 2**16) + (checksum >> 16) #lower half + upper half
        return checksum % 2**16

    def read(self):
        '''Returns a bytes object with all of the Sector's data.'''

        data = self.data
        #adding the footer data
        data += bytes(0xFF4 - len(data)) #padding
        data += self.ID.to_bytes(2, 'little')
        checksum = self.makeChecksum()
        data += checksum.to_bytes(2, 'little')
        data += bytes([0x25, 0x20, 0x01, 0x08]) #validation code
        data += self.saveIndex.to_bytes(4, 'little')
        return data

    def write(self, data):
        '''Adds data from a bytes object to the Sector. If not all of
        the data fits in the Sector, returns the index of the first
        unwritten byte; otherwise, returns -1.'''

        for i,byte in enumerate(data):
            if len(self.data) >= self.maxLength:
                return i
            self.data += bytes([byte])
        return -1

class SaveGame:
    '''A set of 14 Sectors representing a save game. Takes a bytes object as
    its old data.'''

    NUMBER_OF_BOXES = 14
    NUMBER_OF_SECTORS = 14
    LENGTH = Sector.LENGTH * NUMBER_OF_SECTORS #length in bytes

    def __init__(self, data):
        secLen = Sector.LENGTH
        numSecs = self.NUMBER_OF_SECTORS
        box1 = Sector.FIRST_BOX_ID
        box1Off = Sector.FIRST_BOX_OFFSET
        
        secOrder = [data[i*secLen + 0xFF4] for i in range(numSecs)] #list of IDs
        oldData = [data[i*secLen:(i+1)*secLen] for i in range(numSecs)]
        self.oldData = {ID:data for ID,data in zip(secOrder, oldData)}
        
        self.saveIndex = findSaveIndex(data)
        self.sectors = [Sector(i, self.saveIndex) for i in secOrder]
        
        selectedBox = self.oldData[box1][:box1Off]
        self.getSectorByID(box1).write(selectedBox)

    def closeBoxes(self):
        '''Adds the last bits of Box data. Called automatically when the
        final box has been copied or inserted.'''

        lastBox = Sector.LAST_BOX_ID
        
        finalData = self.oldData[lastBox][0x744:0x7D0]
        self.getSectorByID(lastBox).write(finalData)

    def copyOldBox(self, boxNum):
        '''Takes an integer, copies box boxNum from a SaveGame's old data
        to its new data. Make sure all previous boxes have been set first.'''

        boxLen = Box.NEW_LENGTH
        secLen = Sector.VALIDATED_BOX_LENGTH

        sectorID, sectorStart = self.getBoxOffset(boxNum)
        sector1 = self.oldData[sectorID][:secLen]
        sector2 = self.oldData[sectorID+1][:secLen]
        sectorData = sector1 + sector2
        boxData = sectorData[sectorStart:sectorStart + boxLen]
        i = self.getSectorByID(sectorID).write(boxData)
        if i != -1:
            self.getSectorByID(sectorID+1).write(boxData[i:])

        if boxNum == self.NUMBER_OF_BOXES:
            self.closeBoxes()

    def copyOldSector(self, sectorID):
        '''Takes an integer sector ID, copies the SaveGame's old sector into
        its new one. For sectors that contain box data, use copyOldBox
        instead.'''

        sectorData = self.oldData[sectorID]
        self.getSectorByID(sectorID).write(sectorData)

    @staticmethod
    def getBoxOffset(boxNum):
        '''Takes an integer box number, returns a tuple containing
        the sector ID and sector offset of where to start writing
        data for the beginning of box boxNum.'''

        boxLen = Box.NEW_LENGTH
        secLen = Sector.VALIDATED_BOX_LENGTH
        box1 = Sector.FIRST_BOX_ID
        box1Off = Sector.FIRST_BOX_OFFSET
        
        internalStart = (boxNum-1)*boxLen + box1Off
        sectorStart = internalStart % secLen
        sectorID = int(internalStart / secLen) + box1
        return sectorID, sectorStart

    def getSectorByID(self, ID):
        '''Returns the Sector with the given integer ID.'''

        for sector in self.sectors:
            if sector.ID == ID:
                return sector

    def insertBox(self, box, boxNum):
        '''Takes a Box and sets it as a SaveGame's boxNum-th box. Make
        sure all previous boxes have been set first.'''

        sectorID = self.getBoxOffset(boxNum)[0]
        boxData = box.newData()
        i = self.getSectorByID(sectorID).write(boxData)
        if i != -1:
            self.getSectorByID(sectorID+1).write(boxData[i:])

        if boxNum == self.NUMBER_OF_BOXES:
            self.closeBoxes()

    def read(self):
        '''Returns a bytes object representation of the save game.
        Make sure all sectors have been set first.'''

        data = bytes()
        for sector in self.sectors:
            data += sector.read()
        return data

class NewSaveFile:
    '''Contains the entirety of a Generation III save file. Takes a string
    input file name.'''

    def __init__(self, filename):
        self.boxes = [None for i in range(SaveGame.NUMBER_OF_BOXES)]
        
        file = open(filename, 'br')
        data = file.read()
        file.close()

        saveLen = SaveGame.LENGTH
        saveData1 = data[:saveLen]
        saveData2 = data[saveLen:2*saveLen]
        self.miscData = data[2*saveLen:]
        
        index1 = findSaveIndex(saveData1)
        index2 = findSaveIndex(saveData2)
        self.curSaveSlot = 1 if index1 > index2 else 2
        
        if self.curSaveSlot == 1:
            self.curSave = SaveGame(saveData1)
            self.oldSaveData = saveData2
        else:
            self.curSave = SaveGame(saveData2)
            self.oldSaveData = saveData1
            
    def addBox(self, box, boxNum):
        '''Takes a Box and an integer box number, queues the Box for
        writing to the save game.'''

        self.boxes[boxNum-1] = box

    def save(self, filename):
        '''Takes a string file name, writes all of the data to the
        given output file.'''

        for i in range(Sector.FIRST_BOX_ID): #todo: Sectors 0-4 won't always be copied
            self.curSave.copyOldSector(i)
        for i,box in enumerate(self.boxes):
            if box == None:
                self.curSave.copyOldBox(i+1)
            else:
                self.curSave.insertBox(box, i+1)

        newSaveData = self.curSave.read()

        outFile = open(filename, 'bw')
        if self.curSaveSlot == 1:
            outFile.write(newSaveData)
            outFile.write(self.oldSaveData)
        else:
            outFile.write(self.oldSaveData)
            outFile.write(newSaveData)
        outFile.write(self.miscData)
        outFile.close()

class OldSaveFile:
    '''Contains the entirety of a Generation II save file. Takes a string
    input file name.'''

    NUMBER_OF_BOXES = 14
    BOX_OFFSETS = [0x4000, 0x4450, 0x48a0, 0x4cf0, 0x5140, 0x5590, 0x59e0,
                   0x6000, 0x6450, 0x68a0, 0x6cf0, 0x7140, 0x7590, 0x79e0]

    def __init__(self, filename):
        file = open(filename, 'br')
        self.data = file.read()
        file.close()

        self.boxes = [None for i in range(self.NUMBER_OF_BOXES)]
        self.unloadedBoxes = [False for i in range(self.NUMBER_OF_BOXES)]

    def getUnloadedBoxes(self):
        '''Returns an ordered list of all of the unloaded Boxes.'''

        return [box for box in self.boxes if box != None]

    def setTraits(self, game, language, OTGender, secretID):
        '''Sets all of the parameters as traits for every Pokemon in every
        unloaded Box, then gives each Pokemon a personality value and ability.
        This should be used after all wanted Boxes have been unloaded.'''

        for box in self.boxes:
            if box != None:
                box.setTraits(game, language, OTGender, secretID)

    def unloadBox(self, boxNum):
        '''Takes an integer box number, marks the Box for deletion from
        the save file.'''

        start = self.BOX_OFFSETS[boxNum-1]
        self.boxes[boxNum-1] = Box(self.data[start:start+Box.OLD_LENGTH])
        self.unloadedBoxes[boxNum-1] = True
        return self.boxes[boxNum-1]

    def save(self, filename):
        '''Takes a string file name, writes all of the data to the given
        output file.'''

        boxLen = Box.OLD_LENGTH
        boxOffs = self.BOX_OFFSETS
        emptyBoxData = bytes([0x0, 0xFF]) + bytes(boxLen-4) + bytes([0xFF, 0x0])

        newData = bytes()
        newData += self.data[:0x4000]

        i = 1
        for offset,box in zip(boxOffs, self.unloadedBoxes):
            if box:
                newData += emptyBoxData
            else:
                newData += self.data[offset:offset + boxLen]
                
            if i == 7: #padding between boxes 7 and 8
                newData += self.data[0x5e30:0x6000]
            i += 1

        newData += self.data[0x7e30:]
        
        file = open(filename, 'bw')
        file.write(newData)
        file.close()

def findSaveIndex(data):
    '''Takes a bytes object, returns the save game's save index. Can take save
    game data or sector data.'''

    return int.from_bytes(data[0xFFC:0x1000], 'little')

def oldNameTrans(data):
    '''Translates an old encoded name or OT. Takes a bytes object,
    returns a string.'''

    stop = 0x50
    table = {128: 'A', 129: 'B', 130: 'C', 131: 'D', 132: 'E', 133: 'F', 134: 'G', 135: 'H', 136: 'I', 137: 'J', 138: 'K', 139: 'L', 140: 'M', 141: 'N', 142: 'O', 143: 'P', 144: 'Q', 145: 'R', 146: 'S', 147: 'T', 148: 'U', 149: 'V', 150: 'W', 151: 'X', 152: 'Y', 153: 'Z',
             154: '(', 155: ')', 156: ':', 157: ';', 158: '[', 159: ']',
             160: 'a', 161: 'b', 162: 'c', 163: 'd', 164: 'e', 165: 'f', 166: 'g', 167: 'h', 168: 'i', 169: 'j', 170: 'k', 171: 'l', 172: 'm', 173: 'n', 174: 'o', 175: 'p', 176: 'q', 177: 'r', 178: 's', 179: 't', 180: 'u', 181: 'v', 182: 'w', 183: 'x', 184: 'y', 185: 'z',
             225: '\\PK', 226: '\\MN', 227: '-', 230: '?', 231: '!', 232: '.', 127: ' ', 241: '*', 243: '/', 244: ',',
             246: '0', 247: '1', 248: '2', 249: '3', 250: '4', 251: '5', 252: '6', 253: '7', 254: '8', 255: '9'}
    word = ''
    for byte in data:
        if byte == stop:
            return word
        word += table[byte]

def newNameTrans(name, length):
    '''Takes a string name, returns a new translated bytes object, padding up
    to length if necessary.'''

    STOP = 0xFF
    FILL = 0x00
    table = {' ': 0, 'PK': 83, 'MN': 84, '(': 92, ')': 93,
             '0': 161, '1': 162, '2': 163, '3': 164, '4': 165, '5': 166, '6': 167, '7': 168, '8': 169, '9': 170,
             '!': 171, '?': 172, '.': 173, '-': 174, ',': 184, '*': 185, '/': 186,
             'A': 187, 'B': 188, 'C': 189, 'D': 190, 'E': 191, 'F': 192, 'G': 193, 'H': 194, 'I': 195, 'J': 196, 'K': 197, 'L': 198, 'M': 199, 'N': 200, 'O': 201, 'P': 202, 'Q': 203, 'R': 204, 'S': 205, 'T': 206, 'U': 207, 'V': 208, 'W': 209, 'X': 210, 'Y': 211, 'Z': 212,
             'a': 213, 'b': 214, 'c': 215, 'd': 216, 'e': 217, 'f': 218, 'g': 219, 'h': 220, 'i': 221, 'j': 222, 'k': 223, 'l': 224, 'm': 225, 'n': 226, 'o': 227, 'p': 228, 'q': 229, 'r': 230, 's': 231, 't': 232, 'u': 233, 'v': 234, 'w': 235, 'x': 236, 'y': 237, 'z': 238,
             ':': 240}
    MESSAGE_INVALID = "Pokemon {}'s name contains the invalid character {}.\n\nPlease enter a new name for {}.\n\nFor the special combination PK and MN characters, use \\PK and \\MN."
    MESSAGE_LONG = "Pokemon {}'s name is too long.\n\nPlease enter a new name for {}.\n\nFor the special combination PK and MN characters, use \\PK and \\MN."

    data = []
    i = 0
    c = 0
    while i < len(name):
        if name[i] == '\\':
            data.append(table[name[i+1:i+3]])
            i += 3
        elif name[i] not in table:
            from gui import nameHandler
            newName = nameHandler(name, MESSAGE_INVALID.format(name, name[i], name))
            return newNameTrans(newName, length)
        else:
            data.append(table[name[i]])
            i += 1
        c += 1
        if c > Pokemon.NEW_NAME_LENGTH:
            from gui import nameHandler
            newName = nameHandler(name, MESSAGE_LONG.format(name, name))
            return newNameTrans(newName, length)
    if len(data) < length:
        data.append(STOP)
    if len(data) < length:
        data += [FILL for i in range(length - len(data))]
    return bytes(data)

def newSecretID():
    '''Returns a new integer Secret ID.'''
    from random import randint
    
    return randint(0, 2**16 - 1)

def transfer(oldGen2, newGen2, oldGen3, newGen3, oldBoxNums, newBoxNums,
             newGame, language, gender):
    '''Takes 4 string file names, 2 lists of integers, and 3 strings, writes
    2 new save files with the indicated boxes transferred.'''

    oldGame = OldSaveFile(oldGen2)
    for i in oldBoxNums:
        oldGame.unloadBox(i)
    oldGame.setTraits(newGame, language, gender, newSecretID())    
    
    newGame = NewSaveFile(oldGen3)
    for box,num in zip(oldGame.getUnloadedBoxes(), newBoxNums):
        newGame.addBox(box, num)

    oldGame.save(newGen2)
    newGame.save(newGen3)

if __name__ == '__main__':
    import subprocess
    
    oldCrystal = 'C:/Users/Sidnoea/Documents/Video Games/POKEBRIDGE TESTING/Pokemon Crystal (U) [C][!].sav'
    newCrystal = 'C:/Users/Sidnoea/Documents/Video Games/POKEBRIDGE TESTING/Pokemon Crystal (U) [C][!] Test.sav'
    oldRuby = 'C:/Users/Sidnoea/Documents/Video Games/POKEBRIDGE TESTING/Pokemon Ruby.sav'
    newRuby = 'C:/Users/Sidnoea/Documents/Video Games/POKEBRIDGE TESTING/Pokemon Ruby Test.sav'
    
    oldBoxNums = tuple(range(1, 15))
    newBoxNums = tuple(range(1, 15))
    newGame = 'Ruby'
    language = 'English'
    gender = 'male'

    transfer(oldCrystal, newCrystal, oldRuby, newRuby, oldBoxNums, newBoxNums,
             newGame, language, gender)

    emulator = 'C:/Users/Sidnoea/Documents/Video Games/Gameboy and GBA/VisualBoyAdvance-1.7.2/VisualBoyAdvance.exe'
    rom = 'C:/Users/Sidnoea/Documents/Video Games/POKEBRIDGE TESTING/Pokemon Ruby Test.GBA'
    subprocess.Popen([emulator, rom])
