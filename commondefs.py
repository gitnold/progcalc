from enum import Enum, auto
from textual.app import App
import calc_functions

class FileOp(Enum):
    READ=auto()
    WRITE=auto()
    CLEAR=auto()


def trysplit(input: str, output: list, delimiter: str) -> dict:
    try:
        output = [float(s.strip()) for s in input.split(delimiter)]
        return {'output': output, 'user_string': input, 'error': False}
    except ValueError as err:
        return {'output': [], 'user_string': input, 'error': f"Invalid input {err}: Try using a custom expression instead"}

def check_error(input: dict, app: App, op: str):
    result = 0
    if input['output']:
        match op:
            case "Addition":
                result = calc_functions.add(input['output'])
            case "Subtraction":
                result = calc_functions.subtract(input['output'])
            case "Multiplication":
                result = calc_functions.multiply(input['output'])
            case _:
                app.notify("Error", severity='warning', timeout=2.0)
    else:
        #result = calc_functions.custom_equation(input['user_string'])
        result = None
        app.notify(f"Wrong input!", severity='error', timeout=3.0)
    
    return result
