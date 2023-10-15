def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

class Operation:
    def __init__(self, name, symbol, function, description):
        self.name = name
        self.symbol = symbol
        self.function = function
        self.description = description

operation1 = Operation("add", "+", add, "Addition operation")
operation2 = Operation("subtract", "-", subtract, "Subtraction operation")
operation3 = Operation("multiply", "*", multiply, "Multiplication operation")
operation4 = Operation("divide", "/", divide, "Division operation")

obj_list = [operation1, operation2, operation3, operation4]

def main():
    print("Welcome to calculator app. Type help for help. Type exit to exit.")
    running = True
    while running:
        user_input = input()
        if user_input == "exit":
            break
        elif user_input == "help":
            print_help()
        else:
            for operation in obj_list:
                if user_input == operation.name or user_input == operation.symbol:
                    execute_operation(operation)
                    break

def print_help():
    print("Available operations:")
    for operation in obj_list:
        print(f"{operation.name} ({operation.symbol}): {operation.description}")

def execute_operation(operation):
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    result = operation.function(a, b)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()