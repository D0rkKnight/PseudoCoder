import pseudo
import os


def test_write_pseudocode():
    # create a temporary file
    with open("tmp/test_code.py", "w") as f:
        f.write("print('Hello, world!')")

    # call the function to be tested
    pseudo.generate_pseudocode("tmp/test_code.py")

    # check if the pseudocode file was created
    assert os.path.exists("tmp/test_code.pseudo")
