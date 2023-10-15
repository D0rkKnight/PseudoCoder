import os
import ast
import json

from collections import deque


def get_AST(file_path):
    with open(file_path, "r") as file:
        code = file.read()
    AST = ast.parse(code)
    return AST


def get_AST_project(project_path):
    AST_dict = {}

    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)

            if not file_path.endswith(".py"):
                continue

            AST = get_AST(file_path)
            AST_dict[file_path] = AST

    return AST_dict


class SymbolNode:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.children = []

    def to_dict(self):
        # Convert the object to a dictionary
        node_dict = {
            "type": self.type,
            "name": self.name,
            "children": [child.to_dict() for child in self.children],
        }
        return node_dict


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SymbolNode):
            # Serialize YourCustomClass object to a dictionary
            return obj.to_dict()
        return super().default(obj)


def extract_symbols(node):
    name = ""

    if isinstance(node, ast.FunctionDef):
        symbol_type = "function"
        name = node.name
    elif isinstance(node, ast.ClassDef):
        symbol_type = "class"
        name = node.name
    elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
        symbol_type = "variable"
        name = node.id
    else:
        return None

    symbol = SymbolNode(symbol_type, name)

    # Check children since root node is short circuiting
    children = list(ast.iter_child_nodes(node))

    for child in children:
        for descendant in bfs_ast_generator(child):
            if descendant != node:  # Avoid adding the current node as its own child
                child_symbol = extract_symbols(descendant)
                if child_symbol:
                    symbol.children.append(child_symbol)

    return symbol


def get_symbols(AST):
    top_level_symbols = []
    for node in bfs_ast_generator(AST):
        symbol = extract_symbols(node)
        if symbol:
            top_level_symbols.append(symbol)

    return top_level_symbols


def get_symbols_project(AST_dict):
    function_dict = {}

    for file_path, AST in AST_dict.items():
        function_list = get_symbols(AST)
        function_dict[file_path] = function_list

    return function_dict


# Define a generator function to perform BFS traversal on the AST
def bfs_ast_generator(node):
    queue = deque([node])

    while queue:
        current_node = queue.popleft()
        yield current_node  # Yield the current node

        # If a node of interest, do NOT add its children to the queue
        if isinstance(current_node, ast.FunctionDef) or isinstance(
            current_node, ast.ClassDef
        ):
            continue

        # Add child nodes to the queue
        for child in ast.iter_child_nodes(current_node):
            queue.append(child)
