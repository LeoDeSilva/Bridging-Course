from combat.skills.skills import AoeSupportSkill,SupportSkill, PIERCING, FIRE

class Grace(SupportSkill): # multihit
    def __init__(self):
        super().__init__()
        self.skill = "Grace"
        self.range = [1,1,1,1]
        self.formation = [0,0,1,1]

        self.damage_range = [5,10]
        self.damage_type = None


class Blessing(AoeSupportSkill): # multihit
    def __init__(self):
        super().__init__()
        self.skill = "Blessing"
        self.range = [1,1,1,1]
        self.formation = [0,0,1,1]

        self.damage_range = [3,4]
        self.damage_type = None