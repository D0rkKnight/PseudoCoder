import pseudo
import os

# Change working dir to tmp/adventure_game
os.chdir(os.path.join(os.getcwd(), "tmp", "adventure_game"))


pseudo.generate_code("datatypes.pseudo")

print("Done!")
