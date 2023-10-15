def main():
    while True:
        if i_eat_jellybean():
            change_lamp_green()

def change_lamp_green():
    print("Lamp is green")

def i_eat_jellybean():
    user_input = input("Did you eat a jellybean? ")
    if user_input == "jellybean":
        return True
    else:
        return False

if __name__ == "__main__":
    main()