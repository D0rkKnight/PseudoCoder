from datatypes import *


class location:
    name: str
    description: str
    items: list[item]
    exits: list[str]

    def __init__(self, name="", description="", items=[], exits=[]):
        self.name = name
        self.description = description
        self.items = items
        self.exits = exits


# Define items
stone = item("stone", "A small, round stone")
stick = item("stick", "A long, thin stick")
bread = item("bread", "A piece of bread")
water = item("water", "A flask of water")
sword = item("sword", "A sharp sword")
shield = item("shield", "A sturdy shield")

# START_PSEUDO
list_of_locations = []

bogwater = location("Bogwater", "A swampy bog", [stone, stick])
list_of_locations.append(bogwater)

great_hall = location("The Great Hall", "A large hall", [bread, water])
list_of_locations.append(great_hall)

throne_room = location("The Throne Room", "A room with a throne", [sword, shield])
list_of_locations.append(throne_room)

bogwater.exits = [great_hall]
great_hall.exits = [bogwater, throne_room]
throne_room.exits = [great_hall]
# END_PSEUDO
