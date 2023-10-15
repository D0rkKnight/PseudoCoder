class Example:
    def __init__(self, pseudocode, template, output, comments):
        self.pseudocode = pseudocode
        self.template = template
        self.output = output
        self.comments = comments


examples = [
    Example(
        "class A:\n- fields: str_var, int_var",
        "",
        "class A:\n\n    str_var: str\n    int_var: int\n\n    def __init__(self, str_var, int_var):",
        "Note that the types of the fields must be explicitly declared in the output code.",
    ),
    Example(
        "print Hello World",
        'print("Hello World")',
        'print("Hello World")',
        "Note that the template code is returned unchanged because it already matches the pseudocode.",
    ),
    Example(
        "SpawnPool: List(Enemy)\n- Rock",
        "",
        'from datatypes import enemy\n\nSpawnPool = []\n\nrock = enemy("Rock", 10, 5, 1, 0)\nSpawnPool.append(rock)',
        "Note how the enemy type is inferred from the symbols list.",
    ),
]


def example_to_string(example):
    return (
        "<Example>\n    <Pseudocode>\n        "
        + example.pseudocode
        + "\n    </Pseudocode>\n\n    <Template>\n        "
        + example.template
        + "\n    </Template>\n\n    <Output>\n        "
        + example.output
        + "\n    </Output>\n\n    <Comments>\n        "
        + example.comments
        + "\n    </Comments>\n</Example>\n"
    )


def get_examples_str():
    out = ""
    for example in examples:
        out += example_to_string(example)

    return out
