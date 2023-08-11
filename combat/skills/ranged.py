from combat.skills.skills import *


class Dart(Skill): # multihit
    def __init__(self):
        super().__init__()
        self.skill = "Dart"
        self.range = [1,1,1,1]
        self.formation = [0,1,1,1]

        self.damage_range = [3,4]
        self.damage_type = PIERCING #TODO: Poision infliction


class Swiftshot(Skill): # multihit
    def __init__(self):
        super().__init__()
        self.skill = "Swiftshot"
        self.range = [1,1,1,1]
        self.formation = [0,1,1,1]

        self.damage_range = [4,5]
        self.damage_type = PIERCING


class Barrage(Skill):
    def __init__(self):
        super().__init__()
        self.skill = "Barrage"
        self.range = [1,1,1,1]
        self.formation = [0,0,1,1]

        self.damage_range = [2,4]
        self.damage_type = PIERCING
        self.multihit = [2,3]


class Fireball(Skill): # multihit
    def __init__(self):
        super().__init__()
        self.skill = "Fireball"
        self.range = [1,1,1,1]
        self.formation = [0,1,1,1]

        self.damage_range = [9,12]
        self.damage_type = FIRE


class Thunderbolt(Skill): # multihit
    def __init__(self):
        super().__init__()
        self.skill = "Thunderbolt"
        self.range = [1,1,1,1]
        self.formation = [0,0,1,1]

        self.damage_range = [9,12]
        self.damage_type = LIGHTNING


class FlameWhip(Skill): # multihit
    def __init__(self):
        super().__init__()
        self.skill = "Flamewhip"
        self.range = [1,1,0,0]
        self.formation = [1,1,1,0]

        self.damage_range = [3,5]
        self.multihit = [2,3]

        self.damage_type = FIRE


class Inferno(AoeSkill):
    def __init__(self):
        super().__init__()
        self.skill = "Inferno"
        self.range = [1,1,1,1]
        self.formation = [0,1,1,0]

        self.damage_range = [2,4]
        self.damage_type = FIRE


class Nova(AoeSkill):
    def __init__(self):
        super().__init__()
        self.skill = "Nova"
        self.range = [1,1,1,1]
        self.formation = [1,1,1,1]

        self.damage_range = [2,4]
        self.damage_type = MAGIC


class Volley(AoeSkill):
    def __init__(self):
        super().__init__()
        self.skill = "Volley"
        self.range = [1,1,1,1]
        self.formation = [0,0,1,1]

        self.damage_range = [2,2]
        self.multihit = [2,4]
        self.damage_type = PIERCING



#TODO: Incinerate - damage over time, ablaze infliction
#TODO: Poison Dart - inflict poison / sleep effect