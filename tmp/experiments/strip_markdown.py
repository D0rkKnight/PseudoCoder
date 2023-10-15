def strip_code_markdown(code):
    start = 0
    end = len(code)

    # Check start
    if code[:3] == "```":
        start += 3

    # Check end
    if code[-3:] == "```":
        end -= 3

    # if "python" is now at the start, get rid of that too
    if code[start : start + 6] == "python":
        start += 6

    return code[start:end]
