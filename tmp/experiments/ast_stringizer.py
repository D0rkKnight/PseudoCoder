def func_list_to_string(input):
    return ", ".join(input)


def proj_func_list_to_string(input):
    result = ""
    for fname, funclist in input.items():
        result += f"{fname}: {', '.join(funclist)}\n"
    return result
