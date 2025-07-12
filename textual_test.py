import re
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import  Button, Footer, Header, Input, Static, Select, RichLog
from textual import on
import calc_functions
from commondefs import FileOp

#TODO: file reading works for now.
#TODO: work on file writes and clearing history.

LINES = """Addition.
Subtraction.
Division.
Multiplication.
Power.
Percentage.
Custom Expression.""".splitlines()

#current_operation = str()

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

    current_operation = str()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Select.from_values(LINES, prompt="Select Operation")
        yield Footer()
        yield Input(placeholder="Enter operation", id="math-equation")
        yield Execute()
        yield Static(id="output")
        yield RichLog()
    
    def on_ready(self):
        hist_log = self.query_one(RichLog)
        hist_data = calc_functions.manipulate_hist_file(FileOp.READ)
        for item in hist_data:
            hist_log.write(f"History page {item}")

    def action_toggle_dark(self) -> None:
        self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")
        self.notify("Theme changed to dark", severity="information", timeout=3.0)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "evaluate":
            input_box = self.query_one("#math-equation", Input)
            usertext = str(input_box.value)
            #nums_list = usertext.split('+')
            result = float()
            input = list()

            output = self.query_one("#output", Static)
            output.update("entering if block")
            if self.current_operation == "Addition":
                output.update("Enterd if block")
                input = usertext.strip().split('+') #FIXME: list comp doesnt work empty list
                result = calc_functions.add(input)

            match self.current_operation:
                case "Addition":
                    #output.update("Enterd match case")
                    input = usertext.strip().split('+') #FIXME: list comp doesnt work empty list
                    result = calc_functions.add(input)
                case "Subtraction":
                    input =  [float(s.strip()) for s in usertext.split('-')]
                    result = calc_functions.subtract(input)
                case "Division":
                    input =  [float(s.strip()) for s in usertext.split('/')]
                    result = calc_functions.divide(input)
                case "Multiplication":
                    input =  [float(s.strip()) for s in usertext.split('*')]
                    result = calc_functions.multiply(input)
                case "Percentage":
                    input = usertext
                case "Power":
                    input = usertext
                case "Custom Expression":
                    input = usertext
                    result = calc_functions.custom_equation(input)

            #output.update(f"List input is: {type(self.current_operation)}")
            #output.update(f"you typed: {usertext}")
            #output.update(f"Answer is: {result}")
        elif event.button.id == "clearhist":
            self.notify("Clearing history", severity='warning',timeout=1.0)
            status = calc_functions.manipulate_hist_file(FileOp.CLEAR)
            self.notify("Clearing history", severity='warning', timeout=2.0)
            if  len(status) == 0:
                self.notify("History cleared", severity='information', timeout=2.0)
                hist_page = self.query_one(RichLog)
                hist_page.clear()


    
    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        #TODO: use a match case to determine operations to be called.
        self.title = str(event.value)
        self.current_operation = str(event.value)
        input_box = self.query_one("#math-equation", Input)
        #user_text = input_box.value  # 👈 Get value as string
        #output = self.query_one("#output", Static)
        #output.update(f"You typed: {user_text}")




if __name__ == "__main__":
    app = Calculator()
    app.run()
