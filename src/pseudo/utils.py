def strip_code_markdown(code):
    start = 0
    end = len(code)

    # Get top level triple backticks
    top_level = code.split("```")
    if len(top_level) > 1:
        start += len(top_level[0]) + 3
        end -= len(top_level[-1]) + 3

    # Remove Python header next to the first ```
    if code[start : start + 6] == "python":
        start += 6

    return code[start:end]
