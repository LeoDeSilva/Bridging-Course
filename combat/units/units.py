from combat.skills.skills import * 
from colorama import Fore, Style
import json

class Unit:
    def __init__(self, formation):
        self.formation = formation

        self.max_hp = 10
        self.hp = 10

        self.skills = []
        self.buffs = [] 

        self.targetted = False
        self.turn = False
        self.acted = False
        self.corpse = False

        self.resistances = { # multiply damage taken for either resistances or vulnerabilities (vuln > 1, res < 1) 
            BLUNT: 1,
            PIERCING: 1,
            SLASHING: 1,
            FIRE: 1,
            MAGIC: 1,
            LIGHTNING: 1,
        }


    def take_damage(self, damage, damage_type):
        damage_taken = int(damage*self.resistances[damage_type])
        self.hp = max(self.hp-damage_taken, 0)
        return f"{self.unit}({self.formation}) takes {damage} {damage_type} damage. Hp: {self.hp}"

    def heal(self, healing):
        self.hp = min(self.hp + healing, self.max_hp)
        return f"{self.unit}({self.formation}) is healed {healing} hp. Hp: {self.hp}"



class HostileUnit(Unit):
    def __init__(self, formation):
        super().__init__(formation)

    def handle_ai(self, combat_handler):
        acted = False
        while not acted:
            skill = random.choice([skill for skill in self.skills if skill.formation[self.formation] == 1])
            if skill == None: return

            if skill.support and not skill.aoe:
                damaged_units = [i for i in range(len(combat_handler.hostiles)) 
                                 if combat_handler.hostiles[i].hp != combat_handler.hostiles[i].max_hp 
                                 and combat_handler.hostiles[i].hp != 0]

                if len(damaged_units) == 0: continue

                damaged_units = sorted(damaged_units, key=lambda i: combat_handler.hostiles[i].hp)

                formation = damaged_units[0]
                acted, msg = skill.use(combat_handler.hostiles, formation)
                side = combat_handler.hostiles
            else:
                # generate list of all positions in range of attack that contain a living enemy
                available_targets = [i for i in range(len(combat_handler.party)) if skill.range[i] == 1 and combat_handler.party[i].hp > 0]
                if available_targets == []: return

                formation = random.choice(available_targets)

                if skill.support:
                    acted, msg = skill.use(combat_handler.hostiles, formation)
                else:
                    acted, msg = skill.use(combat_handler.party, formation)
                side = combat_handler.party

        side[formation].targetted = True
        combat_handler.clear()
        print(combat_handler)
        print(f"\n{self.unit}({self.formation}) used {skill.skill}.\n{msg}")
        side[formation].targetted = False

        input("proceed?")

    def __str__(self):
        if self.hp <= 0: 
            self.char = "x"
            self.corpse = True

        out = f"{Fore.RED}{self.char}{Style.RESET_ALL}"

        if self.turn: out = f"{Style.BRIGHT}" + out
        return out


#* 0 Theodore Lawrence : Knight 
#  * Skills:
#    * [. o o .] Slash - (3-8) slashing damage
#    * [. . o o] Stab - (3-8) stabbing damage
#    * [. . . o] Bash - (2-5) blunt damage
#  * Resistances:
#    * Piercing: 0.75
#    * Slashing : 1.5
#    * BLUNT : 2

class PartyUnit(Unit):
    def __init__(self, formation):
        super().__init__(formation)

        f = open('descriptors.json')
        descriptors = json.load(f)
        f.close()

        self.name = random.choice(descriptors["forenames"]) + " " + random.choice(descriptors["surnames"])


    def recruitment_msg(self, index):
        print(f"* {Style.BRIGHT}{index if index != None else ''} {self.name} : {self.unit}{Style.RESET_ALL}, hp: {self.hp}")
        print("  * Skills:")

        for skill in self.skills:
            print(f"    * {skill.__str__()}")
        
        #print("* Resistances:")
        #for resistance in self.resistances:
        #    print(f"    * {resistance} : {self.resistances[resistance]}")
        
        print()
    

    def __str__(self):
        if self.hp <= 0: 
            self.char = "x"
            self.corpse = True

        out = f"{Fore.BLUE}{self.char}{Style.RESET_ALL}"
        if self.turn: out = f"{Style.BRIGHT}" + out
        return out
