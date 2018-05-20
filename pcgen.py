#!/usr/bin/env python


import sys
import numpy.random
import json
from adndcharacter import ADnDAbilities, ADnDCharacter


PC_RACES = ['Human', 'Dwarf', 'Elf', 'Gnome', 'Half-Elf', 'Halfling',
            'Half-Orc']
MIN_HITPOINTS = 3
notes = []


def _rolld6():
    return numpy.random.randint(1, 7)


def _roll3d6():
    return _rolld6() + _rolld6() + _rolld6()


def _roll4d6_drop_lowest():
    rolls = [_rolld6(), _rolld6(), _rolld6(), _rolld6()]
    pick = sum(rolls) - min(rolls)
    notes.append("4d6-1d6 = {} {} {} {}".format(rolls[0], rolls[1], rolls[2], rolls[3]))
    # print("---- rolled {} => {}".format(rolls, pick))
    return pick


def roll_high_str():
    return numpy.random.randint(0, 101)


def get_abilities():
    abilities = ADnDAbilities()
    abilities.Strength = _roll4d6_drop_lowest()
    abilities.Intelligence = _roll4d6_drop_lowest()
    abilities.Wisdom = _roll4d6_drop_lowest()
    abilities.Dexterity = _roll4d6_drop_lowest()
    abilities.Constitution = _roll4d6_drop_lowest()
    abilities.Charisma = _roll4d6_drop_lowest()
    return abilities


def get_race(races):
    # p1 = [0.4, 0.125, 0.125, 0.09, 0.15, 0.1, 0.01]
    # p2 = [0.4, 0.125, 0.125, 0.05, 0.2, 0.09, 0.01]
    # rname = numpy.random.choice(PC_RACES, p=p2)
    rname = numpy.random.choice(PC_RACES)
    return rname


def qualify_for_class(class_info, abilities):
    mins = class_info["Min"]
    if "str" in mins:
        if abilities.STR() < mins["str"]:
            return False
    if "int" in mins:
        if abilities.INT() < mins["int"]:
            return False
    if "wis" in mins:
        if abilities.WIS() < mins["wis"]:
            return False
    if "dex" in mins:
        if abilities.DEX() < mins["dex"]:
            return False
    if "con" in mins:
        if abilities.CON() < mins["con"]:
            return False
    if "cha" in mins:
        if abilities.CHA() < mins["cha"]:
            return False
    return True


def get_class(classes, pc):
    """
    Abilitiy best suited for class:
    str: fighter
    int: magic-user
    wis: cleric
    dex: thief
    con:
    cha: 

    wis/cha: druid
    str/wis/cha: paladin
    str/int/wis/con: ranger
    int/dex: illusionist
    str/int/dex: assasin
    str/wis/dex/con: monk

    """
    classes_available = pc.racial_info["Classes"]
    classes_qualify = []
    for cls in classes_available:
        if qualify_for_class(classes[cls], pc.abilities):
            classes_qualify.append(cls)
            notes.append("Qualified for {}".format(cls))
        else:
            notes.append("Not qualified for {}".format(cls))
    if (len(classes_qualify) < 1):
        print("***** ERROR *****")
        print("This PC does not qualify for ANY class!")
        print("Str: {}  Int: {}  Wis: {}  Dex: {}  Con: {}  Cha: {}".format(
              pc_str, pc_int, pc_wis, pc_dex, pc_con, pc_cha))
        return ""
    return numpy.random.choice(classes_qualify)


def get_hitpoints(pc):
    hit_die = pc.class_info["Hit Die"] + 1
    roll = numpy.random.randint(1, hit_die)
    if pc.level == 1:
        if pc.classname == "Ranger":
            roll = roll + numpy.random.randint(1, hit_die)
        if pc.classname == "Monk":
            roll = roll + numpy.random.randint(1, hit_die)
    con_bonus = 0
    if pc.abilities.CON() == 3:
        con_bonus = -2
    if pc.abilities.CON() == 4:
        con_bonus = -1
    if pc.abilities.CON() == 5:
        con_bonus = -1
    if pc.abilities.CON() == 6:
        con_bonus = -1
    if pc.abilities.CON() == 15:
        con_bonus = 1
    if pc.abilities.CON() == 16:
        con_bonus = 2
    if pc.abilities.CON() == 17:
        con_bonus = 2
        if pc.classname == "Fighter":
            con_bonus = 3
    if pc.abilities.CON() == 18:
        con_bonus = 3
        if pc.classname == "Fighter":
            con_bonus = 4
    pc_hp = roll + con_bonus
    if pc.level == 1:
        if pc_hp < MIN_HITPOINTS:
            notes.append("Applying MIN HP, was {} is now {}".format(pc_hp,
                MIN_HITPOINTS))
            pc_hp = MIN_HITPOINTS
    return pc_hp


def apply_racial_ability(pc, ability_name):
    racial_bonus = pc.racial_info["Abilities"]["Bonuses"][ability_name]
    if racial_bonus != 0:
        notes.append("Applying racial bonus of {} for {}".format(racial_bonus,
            ability_name))
    racial_min = pc.racial_info["Abilities"]["Ranges"]["Min"][pc.gender][ability_name]
    racial_max = pc.racial_info["Abilities"]["Ranges"]["Max"][pc.gender][ability_name]
    ability_score = pc.abilities.get_by_name(ability_name) + racial_bonus
    if ability_score < racial_min:
        notes.append("Applying racial min for {}, was {} is now {}".format(
             ability_name.upper(), ability_score, racial_min))
        ability_score = racial_min
    if ability_score > racial_max:
        notes.append("Applying racial max for {}, was {} is now {}".format(
            ability_name.upper(), ability_score, racial_max))
        ability_score = racial_max
    return ability_score


def get_money(pc):
    gold_dice = pc.class_info["Gold"]
    multiplyer = 1
    if pc.classname != "Monk":
        multiplyer = 10
    parts = gold_dice.split('d')
    damt = int(parts[0])
    dtyp = int(parts[1])
    notes.append("Starting gold: {}d{} x {}".format(damt, dtyp, multiplyer))
    gold = 0
    for d in range(damt):
        gold = gold + numpy.random.randint(1, (dtyp + 1))
    gold = gold * multiplyer
    return gold


def calculate_power(pc):
    attrs = pc.abilities.STR() + pc.abilities.INT() + pc.abilities.WIS() + \
        pc.abilities.DEX() + pc.abilities.CON() + pc.abilities.CHA()
    avg = attrs / 6
    power = (avg * pc.level) + pc.hitpoints
    return power


def print_header():
    print("################################################################################")
    print("#                         ADVANCED DUNGEONS AND DRAGONS                        #")
    print("################################################################################")


def main(races, classes):
    pc = ADnDCharacter()
    # Determine abilities (PHB page 9)
    pc.abilities = get_abilities()
    # Determine race (PHB page 13)
    pc.gender = numpy.random.choice(['M', 'F'])
    pc.race = get_race(races)
    pc.racial_info = races[pc.race]
    # apply racial bonuses to abilities
    pc.abilities.Strength = apply_racial_ability(pc, 'str')
    pc.FighterStrengthBonus = 0
    # pc.abilities.Strength = 18
    pc.abilities.Intelligence = apply_racial_ability(pc, 'int')
    pc.abilities.Wisdom = apply_racial_ability(pc, 'wis')
    pc.abilities.Dexterity = apply_racial_ability(pc, 'dex')
    pc.abilities.Constitution = apply_racial_ability(pc, 'con')
    pc.abilities.Charisma = apply_racial_ability(pc, 'cha')
    # Determine class (PHB page 18)
    pc.classname = get_class(classes, pc)
    if len(pc.classname) == 0:
        return pc.classname
    pc.class_info = classes[pc.classname]
    if (str(pc.classname) == "Fighter" and pc.abilities.STR() == 18):
        notes.append("Rolling increased Strength for Fighter with 18 STR")
        pc.abilities.FighterStrengthBonus = roll_high_str()
    # Determine alignment (PHB page 33)
    pc.alignment = numpy.random.choice(classes[pc.classname]["Alignments"])
    # Name
    # Languages
    # Gold
    multiplyer = 1
    if (pc.classname != "Monk"):
        multiplyer = 10
    pc.gold = get_money(pc)
    # Level
    pc.level = 1
    # Hit points
    pc.hitpoints = get_hitpoints(pc)
    # PRINT
    print_header()
    print("Player: _______________________________")
    print("Name:   _______________________________")
    print('Race: {} ({})'.format(pc.race, pc.gender))
    print("Level {} {}".format(pc.level, pc.classname))
    print('Alignment: {}'.format(pc.alignment))
    print("")
    print("Abilities:")
    str_descr = pc.abilities.descr_str(pc.classname == "Fighter")
    if (str(pc.classname) == "Fighter" and pc.abilities.STR() == 18):
        print('Str: {}/{}'.format(pc.abilities.STR(), pc.abilities.STRB()))
        str_descr = pc.abilities.descr_str(isFighter=True)        
        print("    {}".format(str_descr))
    else:
        print('Str: {}'.format(pc.abilities.STR()))
        str_descr = pc.abilities.descr_str() 
        print("    {}".format(str_descr))
    print('Int: {}'.format(pc.abilities.INT()))
    if pc.classname == "Magic-User":
        print("    {}".format(pc.abilities.descr_int(isMagicUser=True)))
    else:
        print("    {}".format(pc.abilities.descr_int()))
    print('Wis: {}'.format(pc.abilities.WIS()))
    print("    {}".format(pc.abilities.descr_wis()))
    print('Dex: {}'.format(pc.abilities.DEX()))
    print("    {}".format(pc.abilities.descr_dex()))
    print('Con: {}'.format(pc.abilities.CON()))
    print("    {}".format(pc.abilities.descr_con()))
    print('Cha: {}'.format(pc.abilities.CHA()))
    print("    {}".format(pc.abilities.descr_cha()))
    print("")
    print("Racial Special Abilities:")
    for sa in pc.racial_info["Special Abilities"]:
        print("  {}".format(sa))
    # clsinfo = classes[pc.classname]
    print("")
    print('Class Specific Weapons and Armor')
    print('  Armor allowed: {}'.format(pc.class_info["Armor"]))
    print('  Shield allowed: {}'.format(pc.class_info["Sheild"]))
    print('  Weapons allowed: {}'.format(pc.class_info["Weapons"]))
    print("")
    print('Weapon Proficiencies:')
    print('  Initial # of Weapons: {}'.format(
        pc.class_info["Proficiencies"]["Initial"]))
    print('  Non-proficiency penalty: {}'.format(
        pc.class_info["Proficiencies"]["Penalty"]))
    print('  Added proficiency: 1/{} levels'.format(
        pc.class_info["Proficiencies"]["Gain"]))
    print("")
    print('Languages: {}'.format(" ".join(pc.racial_info["Languages"])))
    print('Starting GP: {}'.format(pc.gold))
    print('Hit Points: {}'.format(pc.hitpoints))
    power = calculate_power(pc)
    notes.append("POWER: {}".format(power))
    print("")
    print("Notes:")
    for note in notes:
        print("    {}".format(note))
    return pc.classname


def search_for_class(races, classes, desired_class):
    c = ""
    iters = 0
    while True:
        c = main(races, classes)
        iters = iters + 1
        print(" ")
        print(" ")
        if str(c) == desired_class:
            break
    print("After {} interations, a {} has been generated!".format(iters,
          desired_class))


if __name__ == '__main__':
    races_file = open('races.json')
    races = json.load(races_file)
    classes_file = open('classes.json')
    classes = json.load(classes_file)
    if len(sys.argv) > 1:
        search_for_class(races, classes, sys.argv[1])
    else:
        main(races, classes)
