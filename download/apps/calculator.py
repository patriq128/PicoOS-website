def install():
    return {
        "name": "calculator",
        "version": "1.1",
        "autor": "ZiDi"
    }

def main():
    print("Super Calculator")
    first = input("Type the first number: ")
    symbol = input("Type the symbol: ")
    second = input("Type the second number: ")
    if symbol == "+":
        print(int(first) + int(second))
    elif symbol == "-":
        print(int(first) - int(second))
    elif symbol == "*":
        print(int(first) * int(second))
    elif symbol == "/":
        print(int(first) / int(second))
    else:
        print("Wrong symbol")
        print("Use +, -, *, /")