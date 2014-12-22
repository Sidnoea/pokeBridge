pkmnLen = 32 #size of Pokemon in bytes
boxSize = 20 #max number of Pokemon per Box
boxLen = 1102 #size of Box in bytes
OTLen = nameLen = 11 #size of names in bytes
numBoxes = 14
boxStarts = [0x4000,0x4450,0x48a0,0x4cf0,0x5140,0x5590,0x59e0,
             0x6000,0x6450,0x68a0,0x6cf0,0x7140,0x7590,0x79e0]
genders = [0, 31, 31, 31, 31, 31, 31, 31, 31, 31, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 254, 254, 254, 0, 0, 0, 191, 191, 191, 191, 191, 191, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 63, 63, 127, 127, 127, 63, 63, 63, 63, 63, 63, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 255, 255, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 255, 255, 127, 127, 127, 127, 0, 0, 127, 127, 127, 127, 127, 254, 127, 254, 127, 127, 127, 127, 255, 255, 127, 127, 254, 63, 63, 127, 0, 127, 127, 127, 255, 31, 31, 31, 31, 255, 31, 31, 31, 31, 31, 31, 255, 255, 255, 127, 127, 127, 255, 255, 31, 31, 31, 31, 31, 31, 31, 31, 31, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 191, 191, 31, 31, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 31, 31, 127, 127, 127, 255, 127, 127, 127, 127, 127, 127, 127, 191, 191, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 191, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 255, 127, 127, 0, 0, 254, 63, 63, 254, 254, 255, 255, 255, 127, 127, 127, 255, 255, 255]
##Female:Male
##
##00 0:1 Never female
##1F 1:7 Rarely female
##3F 1:3 Sometimes female
##7F 1:1 Even chances
##BF 3:1 Usually female
##FE 1:0 Always female
##FF 0:0 No gender


class Pokemon:
    '''An individual Pokemon. Takes three bytes objects.'''
    
    def __init__(self, data, OTdata, nameData):

        self.species = data[0x0]
        self.item = data[0x1]
        self.moves = [move for move in data[0x2:0x6]]
        self.OTID = (data[0x6] << 8) + data[0x7]
        self.exp = (data[0x8] << 16) + (data[0x9] << 8) + data[0xa]
        
        self.HPEV = (data[0xb] << 8) + data[0xc]
        self.attackEV = (data[0xd] << 8) + data[0xe]
        self.defenseEV = (data[0xf] << 8) + data[0x10]
        self.speedEV = (data[0x11] << 8) + data[0x12]
        self.specialEV = (data[0x13] << 8) + data[0x14]
        self.EVs = [self.HPEV,self.attackEV,self.defenseEV,
                    self.speedEV,self.specialEV]
        
        self.attackIV = (data[0x15] & 0xf0) >> 4
        self.defenseIV = data[0x15] & 0x0f
        self.speedIV = (data[0x16] & 0xf0) >> 4
        self.specialIV = data[0x16] & 0x0f

        IVs = [IV & 1 for IV in [self.attackIV,self.defenseIV,
                                 self.speedIV,self.specialIV]]
        self.HPIV = (IVs[0] << 3) + (IVs[1] << 2) + (IVs[2] << 1) + IVs[3]
        
        self.IVs = [self.HPIV,self.attackIV,self.defenseIV,
                    self.speedIV,self.specialIV]

        self.shiny = (self.defenseIV == self.speedIV == self.specialIV == 10) and self.attackIV in [2,3,6,7,10,11,14,15]
        #todo: gender
        
        PPs = data[0x17:0x1b]
        self.PPups = [(PP & 0b11000000) >> 6 for PP in PPs]
        self.PPvals = [PP & 0b00111111 for PP in PPs]
        
        self.happiness = data[0x1b]
        self.pokerus = data[0x1c] #todo: get data out of this?
        self.caught = data[0x1d:0x1f] #todo: get data out of this
        self.level = data[0x1f]

        self.OT = nameTrans(OTdata)
        self.name = nameTrans(nameData)

class Box:
    '''A box of Pokemon. Takes a bytes object.'''

    def __init__(self, data):
        pkmnStart = boxSize + 2
        OTsStart = pkmnStart + boxSize*pkmnLen
        namesStart = OTsStart + boxSize*OTLen
        
        self.count = data[0x0]
        self.species = [i for i in data[0x1:0x1 + self.count]]
        self.pokemon = []
        for i in range(self.count):
            pkmnData = data[pkmnStart + i*pkmnLen:pkmnStart + (i+1)*pkmnLen]
            OTData = data[OTsStart + i*OTLen:OTsStart + (i+1)*OTLen]
            nameData = data[namesStart + i*nameLen:namesStart + (i+1)*nameLen]
            self.pokemon.append(Pokemon(pkmnData,OTData,nameData))

    def getPokemon(self, slot=None):
        '''Returns the Pokemon in the given slot, taken as a positive
        integer, or a list of all Pokemon if no slot is provided.'''

        if slot == None:
            return self.pokemon
        return self.pokemon[slot - 1]

def nameTrans(data):
    '''Translate an encoded name or OT. Takes a bytes object,
    returns a string.'''
    from string import ascii_uppercase, ascii_lowercase, digits

    stop = 0x50
    upper = {num:let for num,let in zip(range(0x80,0x9a),ascii_uppercase)}
    lower = {num:let for num,let in zip(range(0xa0,0xba),ascii_lowercase)}
    nums = {num:let for num,let in zip(range(0xf6,0x100),digits)}
    misc = {0x7f:' ',0x9a:'(',0x9b:')',0x9c:':',0x9d:';',0x9e:'[',0x9f:']',
            0xe1:'PK',0xe2:'MN',0xe3:'-',0xe6:'?',0xe7:'!',0xe8:'.',0xf1:'*',
            0xf3:'/',0xf4:','}

    table = {}
    table.update(upper)
    table.update(lower)
    table.update(nums)
    table.update(misc)

    word = ''
    for byte in data:
        if byte == stop:
            return word
        word += table[byte]

if __name__ == '__main__':
    file = open('C:/Users/Sidnoea/Documents/Video Games/Gameboy and GBA/Pokemon Crystal/Pokemon Crystal (U) [C][!].sav','br')
    data = file.read()
    file.close()
    box1 = Box(data[boxStarts[0]:boxStarts[0] + boxLen])
    trogdor = box1.getPokemon(7)
    
