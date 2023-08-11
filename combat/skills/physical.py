from combat.skills.skills import *


class Bite(Skill):
    def __init__(self):
        super().__init__()
        self.skill = "Bite"
        self.range = [1,1,0,0]
        self.formation = [1,1,0,0]

        self.damage_range = [2,4]
        self.damage_type = PIERCING


class Cleave(Skill):
    def __init__(self):
        super().__init__()
        self.skill = "Cleave"
        self.range = [1,1,0,0]
        self.formation = [1,1,1,0]

        self.damage_range = [6,9]
        self.damage_type = SLASHING


class Punch(Skill):
    def __init__(self):
        super().__init__()
        self.skill = "Punch"
        self.range = [1,0,0,0]
        self.formation = [1,1,0,0]

        self.damage_range = [2,4]
        self.damage_type = BLUNT


class Stab(Skill):
    def __init__(self):
        super().__init__()
        self.skill = "Stab"
        self.range = [1,0,0,0]
        self.formation = [1,1,0,0]

        self.damage_range = [7,10]
        self.damage_type = PIERCING # affinity bleed?


class Thrust(Skill):
    def __init__(self):
        super().__init__()
        self.skill = "Thrust"
        self.range = [1,1,1,0]
        self.formation = [1,1,0,0]

        self.damage_range = [6,9]
        self.damage_type = PIERCING # affinity bleed?


class Backstab(Skill):
    def __init__(self):
        super().__init__()
        self.skill = "Backstab"
        self.range = [1,1,0,0]
        self.formation = [1,1,0,0]

        self.damage_range = [12,17]
        self.damage_type = PIERCING 


class Cutthroat(Skill):
    def __init__(self):
        super().__init__()
        self.skill = "Cutthroat"
        self.range = [1,1,1,0]
        self.formation = [1,1,0,0]

        self.damage_range = [10,15]
        self.damage_type = SLASHING # affinity bleed?

# AOE Skills


class Slash(AoeSkill):
    def __init__(self):
        super().__init__()
        self.skill = "Slash"
        self.range = [1,1,0,0]
        self.formation = [1,1,0,0]

        self.damage_range = [3,5]
        self.damage_type = SLASHING


class ArcaneSlash(AoeSkill):
    def __init__(self):
        super().__init__()
        self.skill = "Arcaneslash"
        self.range = [1,1,1,0]
        self.formation = [1,1,1,1]

        self.damage_range = [3,5]
        self.damage_type = MAGIC