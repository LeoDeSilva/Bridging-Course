from combat.units.units import HostileUnit
from combat.skills.physical import *
from combat.skills.ranged import *
from combat.skills.support import *
from colorama import Fore, Style
import random

class Bat(HostileUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Bat"
        self.char = "B"

        self.max_hp = 10
        self.hp = 10
        self.skills = [Bite()]


class CorruptedKnight(HostileUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Corrupted Knight"
        self.char = "K"

        self.max_hp = 20
        self.hp = 20
        self.skills = [Slash(), Stab(), Cleave()]


class CorruptedArcher(HostileUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Corrupted Archer"
        self.char = "A"

        self.max_hp = 10
        self.hp = 10
        self.skills = [Punch(), Swiftshot(), Volley(), Barrage()]


class CorruptedMonk(HostileUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Corrupted Monk"
        self.char = "M"

        self.max_hp = 10
        self.hp = 10
        self.skills = [Grace(), Nova(), Blessing()]


#TODO: Warlock, Spider?, Ghost, Troll