import openai
import os
import argparse

import pseudo.utils as utils

# Set up authentication for the OpenAI API
openai.api_key = "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"

GEN_PSEUDO_PROMPT = """ Given the following Python code, write pseudocode for the code and return only that pseudocode."""
GEN_CODE_PROMPT = """ Given the following pseudocode, write Python code for the pseudocode and return only that Python code."""


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
        max_tokens=1000,
    )

    # Extract the generated pseudocode from the API response
    pseudocode = response.choices[0].message.content

    # Write the pseudocode to a new file with the same name as the input file, but with a `.pseudo` extension
    output_file = os.path.splitext(input_file)[0] + ".pseudo"
    with open(output_file, "w") as f:
        f.write(pseudocode)

    print(f"Pseudocode written to {output_file}")


def generate_code(input_file):
    # Read the contents of the input file
    with open(input_file, "r") as f:
        file_contents = f.read()

    messages = [
        {"role": "system", "content": GEN_CODE_PROMPT},
        {"role": "user", "content": file_contents},
    ]

    # Use the OpenAI API to generate code from the file contents
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
    )

    # Extract the generated code from the API response
    code = response.choices[0].message.content
    code = utils.strip_code_markdown(code)

    # Write to python file
    output_file = os.path.splitext(input_file)[0] + ".py"
    with open(output_file, "w") as f:
        f.write(code)

    print(f"Pseudocode written to {output_file}")
