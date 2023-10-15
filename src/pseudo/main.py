import openai
import os
import argparse

import pseudo.utils as utils

# Set up authentication for the OpenAI API
openai.api_key = "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"

GEN_PSEUDO_PROMPT = """ Given the following Python code, write pseudocode for the code and return only that pseudocode."""
GEN_CODE_PROMPT = """ Given the following pseudocode, write Python code for the pseudocode and return only that Python code."""
MOD_CODE_PROMPT = """Given the following Python code and pseudocode, modify the template code as minimally as possible to match the pseudocode and return only the complete Python code. If the template code matches the pseudocode, return the template code."""

WARNING = """IMPORTANT: You must ONLY return complete code.
IMPORTANT: Do NOT summarize parts of the code. Show the code IN FULL."""

MAX_TOKENS = 2000


def cli():
    parser = argparse.ArgumentParser(description="Generate pseudocode from a file")
    parser.add_argument("input_file", help="Path to the input file")
    args = parser.parse_args()

    # generate_pseudocode(args.input_file)
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
        model="gpt-3.5-turbo",
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

    template_exists = template != ""

    if template_exists:
        messages = [
            {"role": "system", "content": MOD_CODE_PROMPT + "\n" + WARNING},
            {"role": "user", "content": "This is the pseudocode: " + pseudocode},
            {"role": "user", "content": "This is the template code: " + template},
        ]

    else:
        messages = [
            {"role": "system", "content": GEN_CODE_PROMPT + "\n" + WARNING},
            {"role": "user", "content": pseudocode},
        ]

    # Use the OpenAI API to generate code from the file contents
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=MAX_TOKENS,
    )

    # Extract the generated code from the API response
    code = response.choices[0].message.content
    code = utils.strip_code_markdown(code)

    # Write to python file
    with open(output_file, "w") as f:
        f.write(code)

    print(f"Pseudocode written to {output_file}")
    print(f"Template exists: {template_exists}")
