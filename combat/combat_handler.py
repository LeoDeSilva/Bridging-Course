import os
# 2 1 *   0 1 2
# A K K | B B A
# –   –   

#Knight: hp: 4
#skills:
#  - slash - (3,8) piercing damage + bleed
#  - smash - (5-10) blunt damage to enemy positions 0,1
#  - defend - negate 50% damage

#What will you do?
#: slash 0

#Bat(0) takes 5 piercing damage, bleed status effect inflicted. Hp: 2


# Knight(0) takes 4 blunt damage from Bat(0), HP: 1

# Archer(2) tales 2 piercing damage from RED: Archer(2), HP remaining: 0
# Archer(2) was killed - their corpse litters the battlefield

#TODO: attacking (and thus destroying) corpses moves all hostiles/units up a position in formation 
    # e.g. K x A A -> K A A _

class CombatHandler:
    def __init__(self, board, party, hostiles):
        self.board = board
        self.party = party
        self.hostiles = hostiles
        self.combat = True

    def clear(self):
        if os.name == "posix": os.system("clear")
        else: os.system("cls")


    def initialise_combat(self):
        if len(self.party) <= 0: 
            input("All your troops were slaughtered, you cannot fight.")
            self.clear()
            return 

        while self.combat:
            for unit in self.party:
                if unit.hp <= 0: continue

                unit.turn = True
                self.combat = self.handle_input(unit)
                unit.turn = False

                if not self.combat: 
                    break
            
            for unit in self.party: unit.acted = False

            for hostile in self.hostiles:
                if hostile.hp <= 0: continue

                hostile.turn = True
                hostile.handle_ai(self)
                hostile.turn = False

            if len(list(filter(lambda u: u.hp > 0, self.party))) == 0: self.combat = False # if no party members alive, quit combat



        # remove all dead units and update indices for existing units
        self.party = list(filter(lambda u: u.hp > 0, self.party))
        for i,unit in enumerate(self.party):
            #unit.hp = unit.max_hp # heal party 
            unit.formation = i 

        if len(self.party) == 0: input("\nYour party was slaughtered, proceed?")
        else: input("\nYou have felled all enemies, proceed?")

        self.clear()

        return self.party


    def get_skill(self, identifier, skills): # return corresponding skill to identifier
        for skill in skills:
            if skill.skill.lower() == identifier:
                return skill
        return None
    

    def handle_input(self, unit):
        while not unit.acted:
            self.clear()
            print(self)

            print(f"{unit.name} : {unit.unit} in position {unit.formation} has HP: {unit.hp}")
            for skill in unit.skills:
                print("  *",skill.__str__(unit))
            print("")

            # input command of processable format (presence check)
            command = ""
            while command == "":
                command = input(":").lower()

                if command == "": 
                    print("I cannot process that command, invalid format")

            match command.split()[0]:
                case "defend": #TODO: mitigate 50% damage
                    unit.acted = True

                case "swap":
                    self.swap_units(command.split()[1:], unit.formation)

                case _:
                    skill = self.get_skill(command.split()[0], unit.skills)

                    if skill and skill.formation[unit.formation] == 1: # in correct formation to use skill 
                        self.use_skill(unit, skill, command.split()[1:])

                    elif skill:
                        print("You cannot perform that skill at this moment, character in incorrect formation, required:", 
                                ",".join([str(i) for i in range(4) if skill.formation[i] == 1])) # return indices of formations to cast skill
                    else:
                        print("I don't recognise that command: ", command)

            input("\nproceed?")

        return len(list(filter(lambda e: e.hp > 0, self.hostiles))) > 0


    def swap_units(self, params, current_unit_formation):
        if params == [] or not params[0].isnumeric():
            print("Expected parameters in format: command <int i>\n")
            return

        swap = int(params[0])

        if swap < 0 or swap >= len(self.party):
            print(f"Parameters out of expected range: (0-{len(self.party)-1})")

        a = self.party[current_unit_formation]
        b = self.party[swap]

        a.formation = swap
        b.formation = current_unit_formation
        a.acted = True
        b.acted = True

        self.party[current_unit_formation] = b
        self.party[swap] = a

        print(self)



    def use_skill(self, unit, skill, command):
        targets = self.hostiles
        if skill.support: targets = self.party

        if skill.aoe:
            unit.acted, msg = skill.use(targets, command)
            print("\n" + msg)
            return

        if len(command) == 0 or not command[0].isnumeric(): 
            print(f"Invalid command format, expected: {skill.skill} <int formation>")
            return

        command = int(command[0])

        if command > len(targets)-1 or command < 0: 
            print(f"Formation position out of range (0-{len(targets) - 1}), got: {command}")
            return

        unit.acted, msg = skill.use(targets, command)

        if not unit.acted:
            print(f"Skill can only reach positions {','.join([str(i) for i in range(4) if skill.range[i] == 1])}, formation position out of range: {command}")
            return

        print("\n" + msg)


    def __str__(self):
        # l1: 2 1 *   0 1 2
        # l2: A K K | B B A
        # l3: ^   ^ 

        l1, l2, l3 = "", "", ""
        for i in range(len(self.party)-1, -1, -1): # iterate through self.party in reverse (step -1)
            l1 += (str(i) if not self.party[i].turn else "*") + " "
            l2 += self.party[i].__str__() + " "
            l3 += "^ " if self.party[i].targetted else "  "

        l1 += "  "
        l2 += "| "
        l3 += "  "

        for i in range(len(self.hostiles)): 
            l1 += (str(i) if not self.hostiles[i].turn else "*") + " "
            l2 += self.hostiles[i].__str__() + " "
        
        return l1 + "\n" + l2 + "\n" + l3