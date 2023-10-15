def strip_code_markdown(code):
    start = 0
    end = len(code)

    # Check start
    if code[:3] == "```":
        start += 3

    # Check end
    if code[-3:] == "```":
        end -= 3

    # Remove Python header next to the first ```
    if "python" in code[start:end].lower():
        end -= code[start:end].lower().index("python")

    return code[start:end]
