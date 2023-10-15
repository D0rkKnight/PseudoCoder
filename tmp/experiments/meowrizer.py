import random


def main():
    while True:
        Meow()


def Meow():
    meow = random.choice(
        ["MEOW", "MEOW MEOW", "MEOW MEOW MEOW", "Mreow", "Mreow", "MOO"]
    )
    print(meow)


if __name__ == "__main__":
    main()
