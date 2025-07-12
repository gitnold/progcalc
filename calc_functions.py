import math
from commondefs import FileOp
# build a parser for custom expression and maybe use for all other functions as well.
# try and see if lambda functions and list comprehension can be used.

calculation_history = list()

def clean_input(input, y):
    math_ops = {
        0: add,
        1: subtract,
        2: multiply,
        3: divide,
        4: square_root,
        5: power,
        6: cube_root,
        7: logarithm,
        8: trigonometry,
        9: custom_equation,
    }
    numbers = list()

    # checking whether input is a list before converting members to int.
    if type(input) is list and y not in (5, 8, 9):
        for item in input:
            numbers.append(int(item))
        answer = math_ops.get(y)(numbers)
    else:
        answer = math_ops.get(y)(input)

    return answer


def add(input):
    return sum(input)


def subtract(input):
    result = input[0]
    for item in input[1:]:
        result -= item

    return result


def multiply(input):
    #TODO: check for exponentiation.
    return math.prod(input)


def divide(input):
    result = input[0]
    for item in input[1:]:
        if item == 0:
            result = "Error! Zero division!!"
        else:
            result /= item

    return result


def square_root(input):
    result = list()
    for item in input:
        result.append(math.sqrt(item))

    return result


def power(input):
    result = list()
    for item in input:
        result.append(
            math.pow(int(item[0]), int(item[1]))
        )  # find a better way of oding this.

    return result


def cube_root(input):
    result = list()
    for item in input:
        result.append(math.cbrt(item))

    return result


def logarithm(input):
    result = list()
    for item in input:
        result.append(math.log10(item))

    return result


def trigonometry(input):
    pass


def custom_equation(input):
    pass

def manipulate_hist_file(option: FileOp) -> list:
    history = str()
    match option:
        case FileOp.READ:
            with open("calc.hist", "r") as f:
                history = f.read()
                #print(type(history))

        case FileOp.WRITE:
            with open("calc.hist", "a") as f:
                for item in calculation_history:
                    f.write(f"{item}\n")

        case FileOp.CLEAR:
            with open("calc.hist", "a") as f:
                f.seek(0)
                f.truncate()

    operations = history.split(sep='\n')
    
    return operations

