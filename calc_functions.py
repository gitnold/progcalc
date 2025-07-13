import math
from commondefs import FileOp
from asteval import Interpreter
import re
# build a parser for custom expression and maybe use for all other functions as well.
# try and see if lambda functions and list comprehension can be used.

regex_patterns = {
    'power': r"(^\d+\s?\^\s?)+\d+$",
    'percentage': r"(^\d+\s?\%\s?)+\d+$",
    'zerodivision': r"[/,\s]0[/,\s]?",

}



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


def divide(input: str):
    filtered_inputs = list()
    result = float()
    FLOAT = r'[+-]?\d+(?:\.\d+)?|\.\d+'
    WS = r'\s*'
    # Non-zero float (no 0, 0.0, 000.00 etc.)
    NON_ZERO_FLOAT = r'(?!0+(?:\.0+)?$)' + FLOAT
    # Pattern: first float, then one or more / valid non-zero float
    safe_div = re.compile(rf'^{WS}{FLOAT}({WS}/{WS}{NON_ZERO_FLOAT})+{WS}$')
    
    if bool(safe_div.fullmatch(input)):
        filtered_inputs = [float(s.strip()) for s in input.split('/')]
        result = filtered_inputs[0]
        for item in filtered_inputs[1:]:
            result /= item
    else:
        result = None


    return result



def custom_equation(input: str):
    evaluator = Interpreter(writer=lambda x: None)

    result = evaluator(input)
    
    return result

def manipulate_hist_file(option: FileOp, calculation_history: list[str]=[]) -> list:
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
            return [True]

        case FileOp.CLEAR:
            with open("calc.hist", "a") as f:
                f.seek(0)
                f.truncate()
            return []

    operations = history.split(sep='\n')
    
    return operations

