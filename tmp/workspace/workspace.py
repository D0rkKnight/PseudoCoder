import pseudo
import pseudo.validator as validator
import os

# Change working dir to tmp/adventure_game
os.chdir(os.path.join(os.getcwd(), "tmp", "workspace"))

# with open("pseudo.txt", "r") as f:
#     pseudo_contents = f.read()

# with open("output.py", "r") as f:
#     template_contents = f.read()

# with open("output.py", "r") as f:
#     output_contents = f.read()

# validation_return = validator.validate_output(
#     pseudo_contents, template_contents, output_contents
# )

# print(validation_return)

pseudo.generate_code("test.pseudo", False)

print("Done!")
