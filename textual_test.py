import re
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import  Button, Footer, Header, Input, Static, Select, RichLog
from textual import on
import calc_functions
from commondefs import FileOp, check_error, trysplit


LINES = """Addition
Subtraction
Division
Multiplication
Power
Percentage
Square Root
Custom Expression""".splitlines()

PLACEHOLDERS = {
    'Addition': "2 + 3 +...+ 4.0",
    'Subtraction': "2 - 4.0 - -4 -...-0.6",
    'Multiplication': "2 * 4.5 * ... * 5",
    'Division': "2 / 3.5 / ... / 4",
    'Power': "2 ** 3",
    'Percentage': "3 % 5",
    'Custom Expression': "(2 + 3) - 5 * 6 / 2",
    'Square Root': "sqrt(25)"
}


class ToastApp(App):
    def on_mount(self) -> None:
        self.notify("A notification has been sent.", severity="information", timeout=3.0)

class Execute(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Evaluate", id="evaluate", variant="success")
        yield Button("Clear History", id="clearhist", variant="error")

        

class Calculator(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "select.tcss"
    current_operation = ""
    calculation_history = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Select.from_values(LINES, prompt="Select Operation")
        yield Footer()
        yield Input(placeholder="Enter operation", id="math-equation")
        yield Execute()
        yield Static(id="output")
        yield RichLog(highlight=True)
    
    def on_mount(self):
        #self.current_operation = ""

        hist_log = self.query_one(RichLog)
        hist_data = calc_functions.manipulate_hist_file(FileOp.READ)
        for item in hist_data:
            hist_log.write(f"{item}")

    def action_toggle_dark(self) -> None:
        self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")
        self.notify("Theme changed to dark", severity="information", timeout=3.0)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "evaluate":
            input_box = self.query_one("#math-equation", Input)
            usertext = str(input_box.value)
            result = float()
            input = list()

            output = self.query_one("#output", Static)
            
            # Debug: Check what operation is selected
            output.update(f"Current operation: {self.current_operation}")
            
            # Use match case only (remove the redundant if block)
            match self.current_operation:
                case "Addition":
                    input = trysplit(usertext, input, '+')
                    result = check_error(input, self, "Addition")
                case "Subtraction":
                    input  = trysplit(usertext, input, '-')
                    result = check_error(input, self, "Subtraction")
                    #result = calc_functions.subtract(input['output'])
                case "Division":
                    result = calc_functions.divide(usertext)
                case "Multiplication":
                    input = trysplit(usertext, input, '*')
                    #result = calc_functions.multiply(input['output'])
                    result = check_error(input, self, "Multiplication")
                case "Percentage":
                    input = usertext
                    result = calc_functions.custom_equation(usertext)
                    
                case "Power":
                    input = usertext
                    result = calc_functions.custom_equation(usertext)
                    
                case "Custom Expression":
                    input = usertext
                    result = calc_functions.custom_equation(input)
                case "Square Root":
                    sqrt_pattern = re.compile(r"^sqrt\(\s*(?:\d+(\.\d+)?|\.\d+)\s*\)$")
                    if bool(sqrt_pattern.fullmatch(usertext)):
                        result = calc_functions.custom_equation(usertext)
                    else:
                        result = None
                        self.notify("Wrong input", severity='error', timeout=3.0)
                case _:  # Default case
                    output.update("No operation selected or invalid operation")
                    return

            # Display the result
            output.update(f"Input: {usertext}, Result: {result}")
            self.manage_history(usertext, result)

            # Add to history
            hist_log = self.query_one(RichLog)
            if result != None:
                hist_log.write(f"{self.current_operation}: {usertext} = {result}")
            else:
                self.notify("Wrong input", severity='error', timeout=3.0)
        
        #TODO: rectify post histroy clearance notification.    
        elif event.button.id == "clearhist":
            self.notify("Clearing history", severity='warning', timeout=1.0)
            status = calc_functions.manipulate_hist_file(FileOp.CLEAR)
            if len(status) == 0:
                self.notify("History cleared", severity='information', timeout=2.0)
                hist_page = self.query_one(RichLog)
                hist_page.clear() 
    
    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        #TODO: use a match case to determine operations to be called.
        self.title = str(event.value)
        self.current_operation = str(event.value)
        input_box = self.query_one("#math-equation", Input)
        input_box.placeholder = f"Example Expression: {PLACEHOLDERS.get(self.title, "Enter Expression: ")}"
    
    def manage_history(self, usertext: str, result):
        if result != None:
            self.calculation_history.append(f"{usertext} = {result}")

        if len(self.calculation_history) >= 5:
            status = calc_functions.manipulate_hist_file(FileOp.WRITE, self.calculation_history)
            if status[0] == True:
                self.notify("History file updated", severity='information', timeout=3.0)
                self.calculation_history.clear()
            else:
                self.notify("Failed to update history file", severity='error', timeout=3.0)



if __name__ == "__main__":
    app = Calculator()
    app.run()
