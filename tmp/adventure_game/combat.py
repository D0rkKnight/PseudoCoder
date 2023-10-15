from datatypes import enemy, player
import random

spawnPool = []
rock = enemy("Rock", 10, 5, 1, 0, 1)
spawnPool.append(rock)

goblin = enemy("Goblin", 20, 10, 2, 10, 5)
spawnPool.append(goblin)

dragon = enemy("Dragon", 50, 20, 5, 50, 10)
spawnPool.append(dragon)

knight = enemy("Knight", 30, 15, 3, 20, 7)
spawnPool.append(knight)


def combat(player):
    enemy = spawnEnemy()
    while player.health > 0 and enemy.health > 0:
        tryAttack(player, enemy)
        tryAttack(enemy, player)


def tryAttack(combatant, recipient):
    if combatant.attack > recipient.defense:
        recipient.health -= combatant.attack - recipient.defense
        print(
            combatant.name
            + " attacks "
            + recipient.name
            + " for "
            + str(combatant.attack - recipient.defense)
            + " damage!"
        )


def spawnEnemy():
    return random.choice(spawnPool)
