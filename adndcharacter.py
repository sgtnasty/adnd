

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
        if an == "DEX":
            return self.Dexterity
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
        return "Hit: {0:+}, Dam: {1:+}, Weight: {2}, Open doors: {3}/6, Bend: {4}%".format(hit, dam, wgt, opn, bar)

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

    def descr_wis(self, isCleric=False):
        maj_adj = -3
        spell_bonus = 0
        spell_fail = 20
        if self.Wisdom > 3:
            maj_adj = -2
        if self.Wisdom > 4:
            maj_adj = -1
        if self.Wisdom > 7:
            maj_adj = 0
        if self.Wisdom > 8:
            maj_adj = 0
            spell_fail = 20
        if self.Wisdom > 9:
            maj_adj = 0
            spell_fail = 15
        if self.Wisdom > 10:
            maj_adj = 0
            spell_fail = 10
        if self.Wisdom > 11:
            maj_adj = 0
            spell_fail = 5
        if self.Wisdom > 12:
            maj_adj = 0
            spell_bonus = "One 1st level"
            spell_fail = 0
        if self.Wisdom > 13:
            maj_adj = 0
            spell_bonus = "One 1st level"
            spell_fail = 0
        if self.Wisdom > 14:
            maj_adj = 1
            spell_bonus = "One 2nd level"
            spell_fail = 0
        if self.Wisdom > 15:
            maj_adj = 2
            spell_bonus = "One 2nd level"
            spell_fail = 0
        if self.Wisdom > 16:
            maj_adj = 3
            spell_bonus = "One 3rd level"
            spell_fail = 0
        if self.Wisdom > 17:
            maj_adj = 4
            spell_bonus = "One 4th level"
            spell_fail = 0
        descr = "Maj Atk Adj: {0:+}".format(maj_adj)
        if isCleric:
            descr = descr + ", Spell Bonus: {}, Chance Spell Fail: {}%".format(spell_bonus, spell_fail)
        return descr

    def descr_dex(self, isThief=False):
        rx_adj = -3
        df_adj = 4
        if self.Dexterity > 3:
            rx_adj = -2
            df_adj = 3
        if self.Dexterity > 4:
            rx_adj = -1
            df_adj = 2
        if self.Dexterity > 5:
            rx_adj = 0
            df_adj = 1
        if self.Dexterity > 14:
            rx_adj = 0
            df_adj = -1
        if self.Dexterity > 15:
            rx_adj = 1
            df_adj = -2
        if self.Dexterity > 16:
            rx_adj = 2
            df_adj = -3
        if self.Dexterity > 17:
            rx_adj = 3
            df_adj = -4
        descr = "Rx/Atk Adj: {0:+},  Def Adj: {1:+}".format(rx_adj, df_adj)
        return descr

    def descr_con(self, isFighter=False):
        hp_adj = -3
        sss = 35
        resur = 40
        if self.Constitution > 3:
            hp_adj = -1
            sss = 40
            resur = 45
        if self.Constitution > 4:
            hp_adj = -1
            sss = 45
            resur = 50
        if self.Constitution > 5:
            hp_adj = -1
            sss = 50
            resur = 55
        if self.Constitution > 6:
            hp_adj = 0
            sss = 55
            resur = 60
        if self.Constitution > 7:
            hp_adj = 0
            sss = 60
            resur = 65
        if self.Constitution > 8:
            hp_adj = 0
            sss = 65
            resur = 70
        if self.Constitution > 9:
            hp_adj = 0
            sss = 70
            resur = 75
        if self.Constitution > 10:
            hp_adj = 0
            sss = 75
            resur = 80
        if self.Constitution > 11:
            hp_adj = 0
            sss = 80
            resur = 85
        if self.Constitution > 12:
            hp_adj = 0
            sss = 85
            resur = 90
        if self.Constitution > 13:
            hp_adj = 0
            sss = 88
            resur = 92
        if self.Constitution > 14:
            hp_adj = 1
            sss = 91
            resur = 94
        if self.Constitution > 15:
            hp_adj = 2
            sss = 95
            resur = 96
        if self.Constitution > 16:
            hp_adj = 2
            if isFighter:
                hp_adj = 3
            sss = 97
            resur = 98
        if self.Constitution > 17:
            hp_adj = 2
            if isFighter:
                hp_adj = 4
            sss = 99
            resur = 100
        return "HP Adj: {0:+},  Sys Shk: {1}%,  Ressurection: {2}%".format(hp_adj, sss, resur)

    def descr_cha(self):
        max_hench = 1
        loyalty = -30
        rx_adj = -25
        if self.Charisma > 3:
            max_hench = 1
            loyalty = -25
            rx_adj = -20
        if self.Charisma > 4:
            max_hench = 2
            loyalty = -20
            rx_adj = -15
        if self.Charisma > 5:
            max_hench = 2
            loyalty = -15
            rx_adj = -10
        if self.Charisma > 6:
            max_hench = 13
            loyalty = -10
            rx_adj = -5
        if self.Charisma > 7:
            max_hench = 3
            loyalty = -5
            rx_adj = 0
        if self.Charisma > 8:
            max_hench = 4
            loyalty = 0
            rx_adj = 0
        if self.Charisma > 9:
            max_hench = 4
            loyalty = 0
            rx_adj = 0
        if self.Charisma > 10:
            max_hench = 4
            loyalty = 0
            rx_adj = 0
        if self.Charisma > 11:
            max_hench = 5
            loyalty = 0
            rx_adj = 0
        if self.Charisma > 12:
            max_hench = 5
            loyalty = 0
            rx_adj = 5
        if self.Charisma > 13:
            max_hench = 6
            loyalty = 5
            rx_adj = 10
        if self.Charisma > 14:
            max_hench = 7
            loyalty = 15
            rx_adj = 15
        if self.Charisma > 15:
            max_hench = 8
            loyalty = 20
            rx_adj = 25
        if self.Charisma > 16:
            max_hench = 10
            loyalty = 30
            rx_adj = 30
        if self.Charisma > 17:
            max_hench = 15
            loyalty = 40
            rx_adj = 35
        descr = "Max Henchmen: {0},  Loyalty Base: {1:+}%,  Rx Adj: {2:+}%".format(max_hench, loyalty, rx_adj)
        return descr


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
        self.isFighter = False
        self.isCleric = False
        self.isMagicUser = False
        self.isThief = False
        self.isMonk = False

