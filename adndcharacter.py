

class ADnDAbilities(object):

    def __init__(self):
        self.Strength = 0
        self.Intelligence = 0
        self.Wisdom = 0
        self.Dexterity = 0
        self.Constitution = 0
        self.Charisma = 0
        self.FighterStrengthBonus = 0

    def STR(self):
        return self.Strength

    def STRB(self):
        return self.FighterStrengthBonus

    def INT(self):
        return self.Intelligence

    def WIS(self):
        return self.Wisdom

    def DEX(self):
        return self.Dexterity

    def CON(self):
        return self.Constitution

    def CHA(self):
        return self.Charisma

    def get_by_name(self, ability_name):
        an = ability_name.upper()
        if an == "STR":
            return self.Strength
        if an == "INT":
            return self.Intelligence
        if an == "WIS":
            return self.Wisdom
        if an == "CON":
            return self.Constitution
        if an == "CHA":
            return self.Charisma
        return 0

    def descr_str(self, isFighter=False):
        hit = -3
        dam = -1
        wgt = -350
        opn = 1
        bar = 0.0
        if self.Strength > 3:
            hit = -2
            dam = -1
            wgt = -250
            opn = 1
            bar = 0
        if self.Strength > 5:
            hit = -1
            dam = 0
            wgt = -150
            opn = 1
            bar = 0
        if self.Strength > 7:
            hit = 0
            dam = 0
            wgt = 0
            opn = 2
            bar = 1
        if self.Strength > 9:
            hit = 0
            dam = 0
            wgt = 0
            opn = 2
            bar = 2
        if self.Strength > 11:
            hit = 0
            dam = 0
            wgt = 100
            opn = 2
            bar = 4
        if self.Strength > 13:
            hit = 0
            dam = 0
            wgt = 200
            opn = 2
            bar = 7
        if self.Strength > 15:
            hit = 0
            dam = 1
            wgt = 350
            opn = 3
            bar = 10
        if self.Strength > 16:
            hit = 1
            dam = 1
            wgt = 500
            opn = 3
            bar = 13
        if self.Strength > 17:
            hit = 1
            dam = 2
            wgt = 750
            opn = 3
            bar = 16
        if isFighter:
            pass
        else:
            return "Hit: {}, Dam: {}, Weight: {}, Open doors: {}/6, Bend: {}%".format(
                hit, dam, wgt, opn, bar)


class ADnDCharacter(object):
    
    def __init__(self):
        self.playername = ""
        self.pcname = ""
        self.abilities = None
        self.gender = ""
        self.race = ""
        self.racial_info = None
        self.class_info = None
        self.classname = ""
        self.alignment = ""
        self.gold = ""
        self.level = 0
        self.racial_abilities = []
        self.languages = []
        self.hitpoints = 0
