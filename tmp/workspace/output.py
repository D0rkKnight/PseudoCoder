class combatant:
    name: str
    health: int
    attack: int
    defense: int

    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense


class player(combatant):
    inventory: list
    gold: int

    def __init__(self, name, health, attack, defense, inventory, gold):
        super().__init__(name, health, attack, defense)
        self.inventory = inventory
        self.gold = gold


class enemy(combatant):
    loot: list
    xp: int

    def __init__(self, name, health, attack, defense, loot, xp):
        super().__init__(name, health, attack, defense)
        self.loot = loot
        self.xp = xp


class item:
    name: str
    description: str
    value: int

    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value


class weapon(item):
    damage: int

    def __init__(self, name, description, value, damage):
        super().__init__(name, description, value)
        self.damage = damage


class armor(item):
    defense: int

    def __init__(self, name, description, value, defense):
        super().__init__(name, description, value)
        self.defense = defense
