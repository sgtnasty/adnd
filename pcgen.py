#!/usr/bin/env python


import sys
import numpy.random
import json


pc_races = ['Human', 'Dwarf', 'Elf', 'Gnome', 'Half-Elf', 'Halfling',
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
    pc_str = _roll4d6_drop_lowest()
    pc_int = _roll4d6_drop_lowest()
    pc_wis = _roll4d6_drop_lowest()
    pc_dex = _roll4d6_drop_lowest()
    pc_con = _roll4d6_drop_lowest()
    pc_cha = _roll4d6_drop_lowest()
    return [pc_str, pc_int, pc_wis, pc_dex, pc_con, pc_cha]


def get_race(races):
    # p1 = [0.4, 0.125, 0.125, 0.09, 0.15, 0.1, 0.01]
    # p2 = [0.4, 0.125, 0.125, 0.05, 0.2, 0.09, 0.01]
    # rname = numpy.random.choice(pc_races, p=p2)
    rname = numpy.random.choice(pc_races)
    return rname


def qualify_for_class(class_info, pc_str, pc_int, pc_wis, pc_dex, pc_con,
                      pc_cha):
    mins = class_info["Min"]
    if "str" in mins:
        if pc_str < mins["str"]:
            return False
    if "int" in mins:
        if pc_int < mins["int"]:
            return False
    if "wis" in mins:
        if pc_wis < mins["wis"]:
            return False
    if "dex" in mins:
        if pc_dex < mins["dex"]:
            return False
    if "con" in mins:
        if pc_con < mins["con"]:
            return False
    if "cha" in mins:
        if pc_cha < mins["cha"]:
            return False
    return True


def get_class(classes, race_info, pc_str, pc_int, pc_wis, pc_dex, pc_con,
              pc_cha):
    classes_available = race_info["Classes"]
    classes_qualify = []
    for cls in classes_available:
        if qualify_for_class(classes[cls], pc_str, pc_int, pc_wis, pc_dex,
                             pc_con, pc_cha):
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


def get_hitpoints(classes_info, pc_class, pc_con, pc_level):
    hit_die = classes_info[pc_class]["Hit Die"] + 1
    roll = numpy.random.randint(1, hit_die)
    if pc_level == 1:
        if pc_class is "Ranger":
            roll = roll + numpy.random.randint(1, hit_die)
        if pc_class is "Monk":
            roll = roll + numpy.random.randint(1, hit_die)
    con_bonus = 0
    if pc_con == 3:
        con_bonus = -2
    if pc_con == 4:
        con_bonus = -1
    if pc_con == 5:
        con_bonus = -1
    if pc_con == 6:
        con_bonus = -1
    if pc_con == 15:
        con_bonus = 1
    if pc_con == 16:
        con_bonus = 2
    if pc_con == 17:
        con_bonus = 2
        if pc_class is "Fighter":
            con_bonus = 3
    if pc_con == 18:
        con_bonus = 3
        if pc_class is "Fighter":
            con_bonus = 4
    pc_hp = roll + con_bonus
    if pc_level == 1:
        if pc_hp < MIN_HITPOINTS:
            notes.append("Applying MIN HP, was {} is now {}".format(pc_hp,
                MIN_HITPOINTS))
            pc_hp = MIN_HITPOINTS
    return pc_hp


def apply_racial_ability(rolled_score, pc_race, ability_name, pc_gender,
                         races):
    race = races[pc_race]
    racial_bonus = race["Abilities"]["Bonuses"][ability_name]
    if racial_bonus != 0:
        notes.append("Applying racial bonus of {} for {}".format(racial_bonus,
            ability_name))
    racial_min = race["Abilities"]["Ranges"]["Min"][pc_gender][ability_name]
    racial_max = race["Abilities"]["Ranges"]["Max"][pc_gender][ability_name]
    ability_score = rolled_score + racial_bonus
    if ability_score < racial_min:
        notes.append("Applying racial min for {}, was {} is now {}".format(
             ability_name.upper(), ability_score, racial_min))
        ability_score = racial_min
    if ability_score > racial_max:
        notes.append("Applying racial max for {}, was {} is now {}".format(
            ability_name.upper(), ability_score, racial_max))
        ability_score = racial_max
    return ability_score


def get_money(gold_dice):
    parts = gold_dice.split('d')
    damt = int(parts[0])
    dtyp = int(parts[1])
    gold = 0
    for d in range(damt):
        gold = gold + numpy.random.randint(1, (dtyp + 1))
    return gold


def calculate_power(pc_str, pc_int, pc_wis, pc_dex, pc_con, pc_cha, pc_level,
                    hp):
    attrs = pc_str + pc_int + pc_wis + pc_dex + pc_con + pc_cha
    avg = attrs / 6
    power = (avg * pc_level) + hp
    return power


def print_header():
    print("################################################################################")
    print("#                         ADVANCED DUNGEONS AND DRAGONS                        #")
    print("################################################################################")


def print_str(pc_str):
    hit = -3
    dam = -1
    wgt = -350
    opn = 1
    bar = 0.0
    if pc_str > 3:
        hit = -2
        dam = -1
        wgt = -250
        opn = 1
        bar = 0
    if pc_str > 5:
        hit = -1
        dam = 0
        wgt = -150
        opn = 1
        bar = 0
    if pc_str > 7:
        hit = 0
        dam = 0
        wgt = 0
        opn = 2
        bar = 1
    if pc_str > 9:
        hit = 0
        dam = 0
        wgt = 0
        opn = 2
        bar = 2
    if pc_str > 11:
        hit = 0
        dam = 0
        wgt = 100
        opn = 2
        bar = 4
    if pc_str > 13:
        hit = 0
        dam = 0
        wgt = 200
        opn = 2
        bar = 7
    if pc_str > 15:
        hit = 0
        dam = 1
        wgt = 350
        opn = 3
        bar = 10
    if pc_str > 16:
        hit = 1
        dam = 1
        wgt = 500
        opn = 3
        bar = 13
    if pc_str > 17:
        hit = 1
        dam = 2
        wgt = 750
        opn = 3
        bar = 16
    print("     Hit: {}, Dam: {}, Weight: {}, Open doors: {}/6, Bend: {}%".format(
        hit, dam, wgt, opn, bar))


def print_str_fighter(pc_str_bonus):
    hit = 1
    dam = 3
    wgt = 1000
    opn = 3
    bar = 20.0
    if pc_str_bonus > 0:
        hit = 1
        dam = 3
        wgt = 1000
        opn = 3
        bar = 20
    if pc_str_bonus > 50:
        hit = 2
        dam = 3
        wgt = 1250
        opn = 4
        bar = 25
    if pc_str_bonus > 75:
        hit = 2
        dam = 4
        wgt = 1500
        opn = 4
        bar = 30
    if pc_str_bonus > 90:
        hit = 2
        dam = 5
        wgt = 2000
        opn = 4
        bar = 35
    if pc_str_bonus > 99:
        hit = 3
        dam = 6
        wgt = 3000
        opn = 5
        bar = 40
    print("     Hit: {}, Dam: {}, Weight: {}, Open doors: {}/6, Bend: {}%".format(
        hit, dam, wgt, opn, bar))


def main(races, classes):
    # Determine abilities (PHB page 9)
    attrs = get_abilities()
    # Determine race (PHB page 13)
    pc_gender = numpy.random.choice(['M', 'F'])
    pc_race = get_race(races)
    # apply racial bonuses to abilities
    pc_str = apply_racial_ability(attrs[0], pc_race, 'str', pc_gender, races)
    pc_str_bonus = 0
    pc_int = apply_racial_ability(attrs[1], pc_race, 'int', pc_gender, races)
    pc_wis = apply_racial_ability(attrs[2], pc_race, 'wis', pc_gender, races)
    pc_dex = apply_racial_ability(attrs[3], pc_race, 'dex', pc_gender, races)
    pc_con = apply_racial_ability(attrs[4], pc_race, 'con', pc_gender, races)
    pc_cha = apply_racial_ability(attrs[5], pc_race, 'cha', pc_gender, races)
    # Determine class (PHB page 18)
    pc_class = get_class(classes, races[pc_race], pc_str, pc_int, pc_wis,
                         pc_dex, pc_con, pc_cha)
    if len(pc_class) == 0:
        return pc_class
    if (str(pc_class) == "Fighter" and pc_str == 18):
        notes.append("Rolling increased Strength for Fighter with 18 STR")
        pc_str_bonus = roll_high_str()
    # Determine alignment (PHB page 33)
    pc_alignment = numpy.random.choice(classes[pc_class]["Alignments"])
    # Name
    # Languages
    # Gold
    pc_gold = get_money(classes[pc_class]["Gold"])
    # Level
    pc_level = 1
    # Hit points
    pc_hp = get_hitpoints(classes, pc_class, attrs[4], pc_level)
    # PRINT
    print_header()
    print("Player: _______________________________")
    print("Name:   _______________________________")
    print('Race: {} ({})'.format(pc_race, pc_gender))
    print("Level {} {}".format(pc_level, pc_class))
    print('Alignment: {}'.format(pc_alignment))
    print("")
    print("Abilities:")
    if (str(pc_class) == "Fighter" and pc_str == 18):
        print('Str: {}/{}'.format(pc_str, pc_str_bonus))
        print_str_fighter(pc_str_bonus)
    else:
        print('Str: {}'.format(pc_str))
        print_str(pc_str)
    print('Int: {}'.format(pc_int))
    print('Wis: {}'.format(pc_wis))
    print('Dex: {}'.format(pc_dex))
    print('Con: {}'.format(pc_con))
    print('Cha: {}'.format(pc_cha))
    print("")
    print("Racial Special Abilities:")
    for sa in races[pc_race]["Special Abilities"]:
        print("  {}".format(sa))
    clsinfo = classes[pc_class]
    print("")
    print('Class Specific Weapons and Armor')
    print('  Armor allowed: {}'.format(clsinfo["Armor"]))
    print('  Shield allowed: {}'.format(clsinfo["Sheild"]))
    print('  Weapons allowed: {}'.format(clsinfo["Weapons"]))
    print("")
    print('Weapon Proficiencies:')
    print('  Initial # of Weapons: {}'.format(
        clsinfo["Proficiencies"]["Initial"]))
    print('  Non-proficiency penalty: {}'.format(
        clsinfo["Proficiencies"]["Penalty"]))
    print('  Added proficiency: 1/{} levels'.format(
        clsinfo["Proficiencies"]["Gain"]))
    print("")
    print('Languages: {}'.format(" ".join(races[pc_race]["Languages"])))
    print('Starting GP: {}'.format(pc_gold))
    print('Hit Points: {}'.format(pc_hp))
    power = calculate_power(pc_str, pc_int, pc_wis, pc_dex, pc_con, pc_cha,
                            pc_level, pc_hp)
    print("POWER: {}".format(power))
    print("")
    print("Notes:")
    for note in notes:
        print("    {}".format(note))
    return pc_class


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
