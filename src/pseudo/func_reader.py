import os
import ast


def get_AST(file_path):
    with open(file_path, "r") as file:
        code = file.read()
    AST = ast.parse(code)
    return AST


def get_AST_project(project_path):
    file_list = os.listdir(project_path)
    AST_dict = {}

    for file in file_list:
        file_path = os.path.join(project_path, file)

        if not file_path.endswith(".py"):
            continue

        AST = get_AST(file_path)
        AST_dict[file_path] = AST

    return AST_dict


def get_function_list(AST):
    function_list = []

    for node in ast.walk(AST):
        if isinstance(node, ast.FunctionDef):
            function_list.append(node.name)

    return function_list


def get_function_list_project(AST_dict):
    function_dict = {}

    for file_path, AST in AST_dict.items():
        function_list = get_function_list(AST)
        function_dict[file_path] = function_list

    return function_dict
