import openai
import os
import argparse
import json

import pseudo.utils as utils
import pseudo.ast_reader as ast_reader

# Set up authentication for the OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

PERSONA = "You are PseudoGPT, an assistant that helps programmers write pseudocode and code. You are given a file with Python code and asked to generate pseudocode for it."
GEN_PSEUDO_PROMPT = """ Given the following Python code, write pseudocode for the code and return only that pseudocode."""

GEN_CODE_PROMPT = """ Given the following pseudocode and tree of symbols, write Python code for the pseudocode and return only that Python code."""
MOD_CODE_PROMPT = """Given the following Python code, pseudocode, and tree of symbols, modify the template code to match the full pseudocode while retaining the overall structure, and return only the complete Python code. If the template code matches the pseudocode fully, return the template code."""

WARNING = """IMPORTANT: Please do not return text before or after the code.
IMPORTANT: Do NOT summarize parts of the code. Show the code IN FULL."""

EXAMPLES = """Below are a series of examples for reference.
Example 1:
Psuedocode:
class A:
- fields: str_var, int_var

Output:
class A:

    # Important! Make variables type safe.
    str_var: str
    int_var: int

    def __init__(self, str_var, int_var):

Note that it did not output any text before or after the code explaining what the code does. It also did not summarize the code. It only showed the code in full.

Example 2:
Psuedocode:
print Hello World

Template:
print("Hello World")

Output:
print("Hello World")

Note that the template code is returned unchanged because it already matches the pseudocode.

Example 3:
Psuedocode:

SpawnPool: List(Enemy)
- Rock
    
Symbols:
"datatypes.py": [{"type": "class", "name": "combatant", "children": [{"type": "variable", "name": "name", "children": []}, {"type": "variable", "name": "health", "children": []}, {"type": "variable", "name": "attack", "children": []}, {"type": "variable", "name": "defense", "children": []}, {"type": "function", "name": "__init__", "children": []}]}, {"type": "class", "name": "enemy", "children": [{"type": "variable", "name": "loot", "children": []}, {"type": "variable", "name": "xp", "children": []}, {"type": "function", "name": "__init__", "children": []}]}]

Output:
from datatypes import enemy

SpawnPool = []

rock = enemy("Rock", 10, 5, 1, 0)
SpawnPool.append(rock)

Note how he enemy type is inferred from the symbols list.

"""

MAX_TOKENS = 4000
LOG_MSG = True


def cli():
    parser = argparse.ArgumentParser(description="Generate pseudocode from a file")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Generate Python code from pseudocode",
    )
    args = parser.parse_args()

    if args.reverse:
        generate_pseudocode(args.input_file)
    else:
        generate_code(args.input_file)


if __name__ == "__main__":
    cli()


def generate_pseudocode(input_file):
    # Read the contents of the input file
    with open(input_file, "r") as f:
        file_contents = f.read()

    messages = [
        {"role": "system", "content": GEN_PSEUDO_PROMPT},
        {"role": "user", "content": file_contents},
    ]

    # Use the OpenAI API to generate pseudocode from the file contents
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=MAX_TOKENS,
    )

    # Extract the generated pseudocode from the API response
    pseudocode = response.choices[0].message.content

    # Write the pseudocode to a new file with the same name as the input file, but with a `.pseudo` extension
    output_file = os.path.splitext(input_file)[0] + ".pseudo"
    with open(output_file, "w") as f:
        f.write(pseudocode)

    print(f"Pseudocode written to {output_file}")


def generate_code(input_file):
    output_file = os.path.splitext(input_file)[0] + ".py"

    # Read the contents of the input file
    with open(input_file, "r") as f:
        pseudocode = f.read()

    # Read the contents of the template file
    template = ""
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            template = f.read()

    # Get list of functions
    proj_ast = ast_reader.get_AST_project(os.getcwd())
    symbol_list = ast_reader.get_symbols_project(proj_ast)

    symbol_str = json.dumps(symbol_list, cls=ast_reader.CustomEncoder)

    messages = [
        {"role": "system", "content": PERSONA},
        {"role": "system", "content": MOD_CODE_PROMPT + "\n" + WARNING},
        {"role": "system", "content": EXAMPLES},
        {"role": "user", "content": "These are available symbols: " + symbol_str},
        {"role": "user", "content": "This is the pseudocode: " + pseudocode},
    ]

    # template_exists = template != ""
    template_exists = False  # No more templating, see what happens
    if template_exists:
        messages.append(
            {"role": "user", "content": "This is the template code: " + template}
        )

    # Use the OpenAI API to generate code from the file contents
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=0.5,
    )

    # Extract the generated code from the API response
    code = response.choices[0].message.content
    code = utils.strip_code_markdown(code)

    # Write to python file
    with open(output_file, "w") as f:
        f.write(code)

    if LOG_MSG:
        for message in messages:
            print(message["role"] + ":")
            print(message["content"] + "\n")

    print(f"Code written to {output_file}")
    print(f"Template exists: {template_exists}")
