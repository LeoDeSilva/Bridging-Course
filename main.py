from procedural_generation.collapse import create_world
from procedural_generation.generative_variables import *


def main():
    LandTile.set_rules(RULES)
    ForrestTile.set_rules(RULES)
    CoastTile.set_rules(RULES)
    SeaTile.set_rules(RULES)
    MountainTile.set_rules(RULES)

    world = create_world(
        WIDTH, HEIGHT, [LandTile, ForrestTile, SeaTile, CoastTile, MountainTile]
    )

    world.run()


if __name__ == "__main__":
    main()
    