
from datatypes import enemy, player, item
import random

# Define items
pebble = item("Pebble", "A small stone", 1)
stick = item("Stick", "A sturdy stick", 2)
dragon_scale = item("Dragon Scale", "A scale from a dragon", 3)
sword = item("Sword", "A sharp sword", 4)

# Define enemies and add them to the SpawnPool
SpawnPool = []
rock = enemy("Rock", 10, 1, 0, [pebble], 1)
SpawnPool.append(rock)
goblin = enemy("Goblin", 15, 2, 1, [pebble, stick], 2)
SpawnPool.append(goblin)
dragon = enemy("Dragon", 20, 3, 2, [pebble, stick, dragon_scale], 3)
SpawnPool.append(dragon)
knight = enemy("Knight", 25, 4, 3, [pebble, stick, dragon_scale, sword], 4)
SpawnPool.append(knight)

# Initialize player
player = player()

def combat():
    enemy = spawnEnemy()
    while player.health > 0 and enemy.health > 0:
        player_choice = input("Player choice?")
        if player_choice == "attack":
            tryAttack(player, enemy)
        else:
            print("Doing nothing this turn.")
        tryAttack(enemy, player)

def tryAttack(combatant, recipient):
    if combatant.attack > recipient.defense:
        recipient.health -= combatant.attack - recipient.defense
        print(combatant.name + " attacks " + recipient.name + " for " + str(combatant.attack - recipient.defense) + " damage!")

def spawnEnemy():
    return random.choice(SpawnPool)
