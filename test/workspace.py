import pseudo

ast = pseudo.get_AST("tmp/func_reader.py")

proj_ast = pseudo.get_AST_project("tmp")

func = pseudo.get_function_list(ast)

proj_func = pseudo.get_function_list_project(proj_ast)

print(ast)
