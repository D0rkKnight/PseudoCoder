import openai
import os
import argparse
import json

import pseudo.utils as utils
import pseudo.ast_reader as ast_reader
import pseudo.examples as examples

# Set up authentication for the OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]
START_EDIT_TAG = "START_PSEUDO"
END_EDIT_TAG = "END_PSEUDO"

PERSONA = "You are PseudoGPT, an assistant that helps programmers write pseudocode and code. You are given a file with Python code and asked to generate pseudocode for it."
GEN_PSEUDO_PROMPT = """ Given the following Python code, write pseudocode for the code and return only that pseudocode."""

GEN_CODE_PROMPT = """ Given the following pseudocode and tree of symbols, write Python code for the pseudocode and return only that Python code."""
MOD_CODE_PROMPT = """Given the following Python code, pseudocode, and tree of symbols, modify the template code to match the pseudocode while retaining the overall structure, and return only the Python code. If the template code matches the pseudocode fully, return the template code."""

RETURN_FULL = """ Please return the code for the entire file."""
RETURN_EDIT = f""" Since # {START_EDIT_TAG} and # {END_EDIT_TAG} are present, you should only edit and return code within those lines. That is, please return code for only the section between # {START_EDIT_TAG} and # {END_EDIT_TAG}.
"""

WARNING = """IMPORTANT: Please do not return text before or after the code.
IMPORTANT: Do NOT summarize parts of the code. Show the code IN FULL."""

EXAMPLES = examples.get_examples_str()

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
    parser.add_argument("--dry", action="store_true", help="Dry run")
    args = parser.parse_args()

    if args.reverse:
        generate_pseudocode(args.input_file, args.dry)
    else:
        generate_code(args.input_file, args.dry)


if __name__ == "__main__":
    cli()


def generate_pseudocode(input_file, dry):
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


def generate_code(input_file, dry):
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

    system_msg = [
        {"role": "system", "content": PERSONA},
        {"role": "system", "content": MOD_CODE_PROMPT + "\n" + WARNING},
        {"role": "system", "content": EXAMPLES},
    ]

    # Check if start and end edit tags exist
    if START_EDIT_TAG in template and END_EDIT_TAG in template:
        system_msg.append({"role": "system", "content": RETURN_EDIT})
    else:
        system_msg.append({"role": "system", "content": RETURN_FULL})

    usr_msg = [
        {"role": "user", "content": "These are available symbols: " + symbol_str},
        {"role": "user", "content": "This is the pseudocode: " + pseudocode},
    ]

    template_exists = template != ""
    if template_exists:
        usr_msg.append(
            {"role": "user", "content": "This is the template code: " + template}
        )

    messages = system_msg + usr_msg

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
    if not dry:
        with open(output_file, "w") as f:
            f.write(code)

    if LOG_MSG:
        for message in messages:
            print(message["role"] + ":")
            print(message["content"] + "\n")
        print("Code:")
        print(code)

    print(f"Code written to {output_file}")
    print(f"Template exists: {template_exists}")
