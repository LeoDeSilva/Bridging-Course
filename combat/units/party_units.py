from combat.units.units import PartyUnit
from combat.skills.physical import *
from combat.skills.ranged import *
from combat.skills.support import *
from colorama import Fore, Style


class Knight(PartyUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Knight"
        self.char = "K"

        self.max_hp = 20
        self.hp = 20
        self.skills = [Slash(), Stab(), Cleave()]

        self.resistances[BLUNT] =  0.5
        self.resistances[PIERCING] = 1.25
        self.resistances[SLASHING] = 0.75


class Rogue(PartyUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Rogue"
        self.char = "R"

        self.max_hp = 7
        self.hp = 7
        self.skills = [Cutthroat(), Backstab(), Dart()]


class Spearman(PartyUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Spearman"
        self.char = "S"

        self.max_hp = 15
        self.hp = 15
        self.skills = [Stab(), Thrust()]


# Ranged Units

class Archer(PartyUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Archer"
        self.char = "A"

        self.max_hp = 10
        self.hp = 10
        self.skills = [Punch(), Swiftshot(), Volley(), Barrage()]


class Pyromancer(PartyUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Pyromancer"
        self.char = "P"

        self.hp = 13
        self.max_hp = 13

        self.skills = [Punch(), Fireball(), FlameWhip(), Inferno()]


class Wizard(PartyUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Wizard"
        self.char = "W"

        self.hp = 15
        self.max_hp = 15

        self.skills = [Nova(), Thunderbolt(), ArcaneSlash()]

# Support Units

class Monk(PartyUnit):
    def __init__(self, formation):
        super().__init__(formation)
        self.unit = "Monk"
        self.char = "M"

        self.hp = 12
        self.max_hp = 12
        self.skills = [Grace(), Blessing(), Nova()]

# TODO: Mage, Necromancer