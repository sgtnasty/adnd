#!/usr/bin/env python


import numpy.random


class Abilities(object):
    def __init__(self):
        self.STR = 0
        self.INT = 0
        self.WIS = 0
        self.DEX = 0
        self.CON = 0
        self.CHA = 0

    def power(self):
        p = self.STR + self.INT + self.WIS + self.DEX + self.CON + self.CHA
        power = float(p) / 6.0
        return power

    def print_r(self):
        print("STR: {}".format(self.STR))
        print("INT: {}".format(self.INT))
        print("WIS: {}".format(self.WIS))
        print("DEX: {}".format(self.DEX))
        print("CON: {}".format(self.CON))
        print("CHA: {}".format(self.CHA))
        print("     avg = {}".format(self.power()))

    def csv(self):
        return "{},{},{},{},{},{}".format(self.STR, self.INT, self.WIS, self.DEX, self.CON, self.CHA)


def _rolld6():
    return numpy.random.randint(1, 7)


def _roll3d6():
    return _rolld6() + _rolld6() + _rolld6()


def rolld_nd6_drop_lowest(ndice):
    rolls = []
    for n in range(ndice):
        rolls.append(_rolld6())
    rolls.sort(reverse = True)
    return rolls[0] + rolls[1] + rolls[2]


def method1():
    a = Abilities()
    a.STR = rolld_nd6_drop_lowest(4)
    a.INT = rolld_nd6_drop_lowest(4)
    a.WIS = rolld_nd6_drop_lowest(4)
    a.DEX = rolld_nd6_drop_lowest(4)
    a.CON = rolld_nd6_drop_lowest(4)
    a.CHA = rolld_nd6_drop_lowest(4)
    return a


def method2():
    a = Abilities()
    rolls = []
    for n in range(12):
        rolls.append(_roll3d6())
    rolls.sort(reverse = True)
    a.STR = rolls[0]
    a.INT = rolls[1]
    a.WIS = rolls[2]
    a.DEX = rolls[3]
    a.CON = rolls[4]
    a.CHA = rolls[5]
    return a


def _method3():
    rolls = []
    for n in range(6):
        rolls.append(_roll3d6())
    rolls.sort(reverse = True)
    return rolls[0]


def method3():
    a = Abilities()
    a.STR = _method3()
    a.INT = _method3()
    a.WIS = _method3()
    a.DEX = _method3()
    a.CON = _method3()
    a.CHA = _method3()
    return a


def method4():
    rolls = []
    for n in range(12):
        a = Abilities()
        a.STR = _roll3d6()
        a.INT = _roll3d6()
        a.WIS = _roll3d6()
        a.DEX = _roll3d6()
        a.CON = _roll3d6()
        a.CHA = _roll3d6()
        rolls.append(a)
    max_roll = rolls[0]
    for roll in rolls:
        if roll.power() > max_roll.power():
            max_roll = roll
    return a
    print("Method 4")
    max_roll.print_r()


def main():
    a1 = method1()
    a2 = method2()
    a3= method3()
    a4 = method4()
    fp = open('save.csv', 'a+')
    fp.write(a1.csv())
    fp.write('\n')
    fp.write(a2.csv())
    fp.write('\n')
    fp.write(a3.csv())
    fp.write('\n')
    fp.write(a4.csv())
    fp.write('\n')
    fp.close()    


if __name__ == '__main__':
    main()