from items.satchel import Satchel
from combat.units.party_units import *
from colorama import Fore, Style
import random
import os


def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


class Player:
    def __init__(self, world, x=-1, y=-1):
        self.world = world

        self.party_units = [Spearman, Knight, Archer, Pyromancer, Rogue, Monk, Wizard]
        self.recruits = [random.choice(self.party_units)(None) for _ in range(4)]  # randomly populate recruit panel
        self.party = []

        self.satchel = Satchel()

        self.x = x
        self.y = y

    def handle_input(self):
        screen = self.world.get_screen(self.x, self.y)
        print(screen.accessed_msg())
        print(screen.generate_surroundings_msg(self.world))
        screen.visited = True

        cmd = ""
        while cmd == "":
            cmd = input(":")

        cmd = cmd.split(" ")
        print()

        match cmd[0]: 
            case "go":
                self.go_cmd(cmd[1:])
            case "recruit":
                self.recruit_cmd()            
            case "formation":
                self.rearrange_party()
            case "enter":
                if screen.entrance:
                    self.enter_screen(screen)
            case "take":
                self.take_item(screen, cmd[1:])
            case "use":
                self.satchel.use_item(self.world, cmd[1])
                input("proceed?")
            case "leave":
                self.world.running = False
            case "quit":
                self.world.running = False
            case _: 
                print("\nI don't recognise the command: ", cmd[0])
                input("proceed?")

    def take_item(self, screen, params):
        for item in screen.items:
            if item.item == params[0]:
                self.satchel.store_item(item)
                screen.items.remove(item)

                print(f"Taken {item.item}")
                print(self.satchel)
                print("")
                input("proceed?")
                return 
        
        print(f"{params[0]} cannot be picked up")
        input("proceed")
        print()

    def enter_screen(self, screen):
        player_copy = Player(screen.dungeon, screen.dungeon.init_x, screen.dungeon.init_y)

        # Copy players party and satchel to new player instance for dungeon to share items and party members
        screen.dungeon.player = player_copy 
        screen.dungeon.player.party = self.party
        screen.dungeon.player.satchel = self.satchel
        screen.dungeon.player.world = screen.dungeon
        screen.dungeon.initialise()

        screen.dungeon.run()
        self.party = screen.dungeon.player.party
        self.satchel = screen.dungeon.player.satchel
        self.satchel.world = self.world

    def recruit_cmd(self):
        if len(self.recruits) == 0: 
            print("You have no recruits available, ")
            input("proceed?")
            return
        
        running = True
        while running and len(self.recruits) > 0:
            clear()
            for i, recruit in enumerate(self.recruits):  # display info on each recruit
                recruit.recruitment_msg(i)

            print("Which recruit do you desire?")
            recruit = ""
            while not recruit.isnumeric() or int(recruit) < 0 or int(recruit) >= len(self.recruits):  # until inputted value within indices of party
                recruit = input(":")
                if recruit in ("done", "quit", "none"): 
                    running = False
                    break

            if not running:
                break

            recruit = int(recruit)

            self.recruit_unit(self.recruits[recruit])

        clear()
        reformat = input("\nDo you desire to modify your party formation?\n")

        if reformat in ("y", "yes"):
            self.rearrange_party()

    def recruit_unit(self, recruit):
        # if full party, select unit to replace
        if len(self.party) == 4:
            clear()
            print("You currently have a full party. Which unit will you replace?\n")

            recruit.recruitment_msg(None)
            print("for\n")

            for i, unit in enumerate(self.party):
                unit.recruitment_msg(i)

            # generate index of replaced value, ensure is integer, and within bounds of party indices
            to_replace = ""
            while not to_replace.isnumeric() or int(to_replace) < 0 or int(to_replace) >= len(self.party):
                to_replace = input(":")

                if to_replace == "quit":
                    return

            to_replace = int(to_replace)

            recruit.formation = to_replace
            self.party[to_replace] = recruit
            self.recruits.remove(recruit)

            print(f"{recruit.name} : {recruit.unit} has replaced {self.party[to_replace].name} : {self.party[to_replace].unit}")
            input("proceed?")
            return

        # otherwise append and rearrange party
        recruit.formation = len(self.party)
        self.party.append(recruit)
        self.recruits.remove(recruit)
        return

    def rearrange_party(self):
        if len(self.party) <= 1:
            print("Your party is too small to rearrange")
            input("proceed?")
            return

        print("")
        running = True
        while running:
            # output party information and indices + units
            l1, l2 = "", ""
            for i in range(len(self.party)-1, -1, -1):  # iterate through self.party in reverse (step -1)
                l1 += str(i) + " "
                l2 += self.party[i].__str__() + " "
            print(l1 + "\n" + l2)

            command = ""
            while command == "":
                command = input(":").lower()
                if command == "": 
                    print("I cannot process that command, invalid format\n")

            if command in ("quit", "done"):
                return

            params = command.split()[1:]

            if not params:
                print("Expected parameters in format: command <int i, int j>\n")
                continue

            params = params[0].split(",")  # if two integer indices are not comma separated (format check)
            if len(params) < 2 or not params[0].isnumeric() or not params[1].isnumeric(): 
                print("Expected parameter format: command <i,j>\n")
                continue

            params = (int(params[0]), int(params[1]))

            if params[0] < 0 or params[1] < 0 or params[1] >= len(self.party) or params[0] >= len(self.party):  # if either index is outside bounds of party
                print(f"Parameters out of expected range: (0-{len(self.party)-1})")

            if command.split()[0] == "swap":
                a = self.party[params[0]]
                b = self.party[params[1]]

                a.formation = params[1]
                b.formation = params[0]

                self.party[params[0]] = b
                self.party[params[1]] = a
            else:
                print("I don't recognise that command")

            print()

    def go_cmd(self, params):
        x = self.x
        y = self.y
        
        match params[0]:
            case "north": y -= 1
            case "south": y += 1
            case "west": x -= 1
            case "east": x += 1
            case _: 
                print("I don't recognise the direction: ", params[0])
                input("continue?")
                return

        # determine validity of move position and return message accordingly
        if self.world.is_valid_location(x, y):
            if self.world.get_screen(x, y).walkable:
                self.x = x
                self.y = y
            else:
                print(self.world.get_screen(x, y).inaccessible_msg)
                input("continue?")
        else:
            print("You find yourself impeded by the presence of a towering wall encroaching far into the heavens")
            input("continue?")

        self.world.reveal_surrounding_tiles(self.x, self.y)

    def __str__(self):
        return f"{Fore.LIGHTMAGENTA_EX}P{Style.RESET_ALL}"
