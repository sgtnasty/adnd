

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
                if self.FighterStrengthBonus > 0:
                    hit = 1
                    dam = 3
                    wgt = 1000
                    opn = 3
                    bar = 20
                if self.FighterStrengthBonus > 50:
                    hit = 2
                    dam = 3
                    wgt = 1250
                    opn = 4
                    bar = 25
                if self.FighterStrengthBonus > 75:
                    hit = 2
                    dam = 4
                    wgt = 1500
                    opn = 4
                    bar = 30
                if self.FighterStrengthBonus > 90:
                    hit = 2
                    dam = 5
                    wgt = 2000
                    opn = 4
                    bar = 35
                if self.FighterStrengthBonus > 99:
                    hit = 3
                    dam = 6
                    wgt = 3000
                    opn = 5
                    bar = 40
        return "Hit: {}, Dam: {}, Weight: {}, Open doors: {}/6, Bend: {}%".format(
            hit, dam, wgt, opn, bar)

    def descr_int(self, isMagicUser=False):
        addl = 0
        chance_know_spell = 35
        min_spells = 4
        max_spells = 6
        if self.Intelligence > 7:
            addl = 1
        if self.Intelligence > 9:
            addl = 2
        if self.Intelligence > 11:
            addl = 3
        if self.Intelligence > 13:
            addl = 4
        if self.Intelligence > 14:
            addl = 5
        if self.Intelligence > 16:
            addl = 6
        if self.Intelligence > 17:
            addl = 7
        descr = "No Additl Lang: {}".format(addl)
        if isMagicUser:
            if self.Intelligence > 9:
                chance_know_spell = 45
                min_spells = 5
                max_spells = 7
            if self.Intelligence > 12:
                chance_know_spell = 55
                min_spells = 6
                max_spells = 9
            if self.Intelligence > 14:
                chance_know_spell = 65
                min_spells = 7
                max_spells = 11
            if self.Intelligence > 16:
                chance_know_spell = 75
                min_spells = 8
                max_spells = 14
            if self.Intelligence > 17:
                chance_know_spell = 86
                min_spells = 9
                max_spells = 18
            if self.Intelligence > 18:
                chance_know_spell = 95
                min_spells = 10
                max_spells = "All"
            descr = descr + ", Chance know spell: {}%, Min Spells/Lvl: {}, Max Spells/Lvl: {}".format(chance_know_spell, min_spells, max_spells)
        return descr

    def descr_wis(self):
        return ""

    def descr_dex(self):
        return ""

    def descr_con(self):
        return ""

    def descr_cha(self):
        return ""


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
