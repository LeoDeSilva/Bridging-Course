from colorama import Fore, Style
import random


BLUNT = "blunt"
PIERCING = "piercing"
SLASHING = "slashing"
FIRE = "fire"
MAGIC = "magic"
LIGHTNING = "lightning"

#TODO: Inflictions, Ranged

class Skill:
    def __init__(self):
        self.skill = ""
        self.range = [] # positions that can be reached
        self.formation = [] # formation required to cast skill

        self.damage_range = []
        self.damage_type = "" # damage type
        self.multihit = [1,1]

        self.aoe = False 
        self.support = False
        self.passive = False

        # + affinities e.g. piercing may inflict bleed attribute


    def use(self, units, formation): # return True if successful skill use (determines whether user reinput command if error)
        if self.range[formation] != 1: return False, ""
        if units[formation] == None: return False, ""

        damage = random.randint(self.damage_range[0], self.damage_range[1])
        msg = ""

        if self.multihit[1] > 1: 
            hits = random.randint(self.multihit[0], self.multihit[1])
            damage *= hits
            msg += f"{self.skill} landed {hits} times\n"

        msg += units[formation].take_damage(damage, self.damage_type)

        return True, msg


    def __str__(self, unit=None):
        formation = "[" + " ".join(["." if self.formation[i] == 0 else "o" for i in range(len(self.formation)-1, -1, -1)]) + "]"
        ranges = "[" + " ".join(["." if self.range[i] == 0 else "o" for i in range(len(self.range))]) + "]"
        out = f"{formation} {self.skill}: ({self.damage_range[0]}-{self.damage_range[1]}) {self.damage_type} damage to positions {ranges}"
        if unit and self.formation[unit.formation] != 1: out = Style.DIM + out + Style.RESET_ALL
        return out



class PassiveSkill(Skill): # buffs
    def __init__(self):
        super().__init__()
        self.passive = True

    def use(self, units, formation):
        pass


class AoeSkill(Skill):
    def __init__(self):
        super().__init__()
        self.aoe = True

    def use(self, units, formation):
        #if self.range[formation] != 1: return False, ""
        #if units[formation] == None: return False, ""

        msg = ""
        damage = random.randint(self.damage_range[0], self.damage_range[1])

        if self.multihit[1] > 1: 
            hits = random.randint(self.multihit[0], self.multihit[1])
            damage *= hits
            msg += f"{self.skill} landed {hits} times\n"

        for i, unit in enumerate(units):
            if self.range[i] == 1 and not unit.corpse:
                msg += unit.take_damage(damage, self.damage_type) + "\n"

        return True, msg


class SupportSkill(Skill):
    def __init__(self):
        super().__init__()
        self.support = True

    def use(self, units, formation):
        healing = random.randint(self.damage_range[0], self.damage_range[1])
        if units[formation].corpse:
            return False, ""
        return True, units[formation].heal(healing)

class AoeSupportSkill(Skill):
    def __init__(self):
        super().__init__()
        self.support = True
        self.aoe = True

    def use(self, units, formation):
        msg = ""
        healing = random.randint(self.damage_range[0], self.damage_range[1])

        if self.multihit[1] > 1: 
            hits = random.randint(self.multihit[0], self.multihit[1])
            healing *= hits
            msg += f"{self.skill} landed {hits} times\n"

        for i, unit in enumerate(units):
            if self.range[i] == 1 and not unit.corpse:
                msg += unit.heal(healing) + "\n"

        return True, msg