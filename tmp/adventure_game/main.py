# Import necessary modules
import time
import random
import combat
import datatypes


# Define game functions
def display_intro():
    # Display game introduction
    print("welcome to the adventure game")


def get_player_name():
    # Get player name from user input
    print("what is your name")
    player_name = input()
    return player_name


def start_game():
    # Start the game
    combat.combat(player)


def play_again():
    # Ask player if they want to play again
    print("do you want to play again")
    play_again = input()
    return play_again


# Define game variables
player = datatypes.player("", 100, 10, 5, [], 0)
game_over = False

# Call game functions
display_intro()
player.name = get_player_name()

while not game_over:
    start_game()
    game_over = not play_again()

# Display game over message
print("Game Over")
