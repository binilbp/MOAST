from libagent import get_context_commands
import asyncio 
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Static, TabbedContent, TabPane, Label, Input, TextArea, Button
from textual.containers import Container, Vertical, VerticalScroll, Horizontal


class NameContainer(Container):
    #ASCII Art container

    def compose(self) -> ComposeResult:
        with open("linquix_ascii.txt", "r") as artfile:
            art = artfile.read()
            yield Label(art, id="ascii")



class Terminal(VerticalScroll):
    def compose(self) -> ComposeResult:
        inputbox = Input(
                placeholder = "Give your instruction here. Press enter to send instructions",
                id = "userprompt"
        )
        inputbox.border_title = "Prompt"
        yield inputbox

        agentbox = TextArea()
        terminalbox =  TextArea(
                id = "terminaldisplay",
                disabled = True
        )
        
        terminalbox.border_title = "Terminal"
        yield terminalbox
        yield ExecutionBox()


    @on (Input.Submitted)
    async def send_user_input(self) -> None:
        inputbox = self.query_one(Input)
        user_input = inputbox.value
        inputbox.value = ""                                        #clear for nxt input

        response = get_context_commands(user_input = user_input, model = 'llama3.2')

        command_area = self.query_one(TextArea)
        command_area.disabled = True
        command_area.clear()

        for chunk in response:
            if 'content' in chunk['message']:
                command_area.insert(chunk['message']['content'])
        command_area.insert("\n")
        #enable editing in the generated content
        command_area.disabled = False
        #move the focus to command now
        command_area.focus()

class ExecutionBox(Horizontal):
    def compose(self) -> ComposeResult:
        yield (Button.success("Execute", flat = True))
        yield (Button.error("Stop", flat = True ))
        

class Body(VerticalScroll):
    # main body container of the app

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Terminal", id = "terminal"):
                yield Terminal()

            with TabPane("Server", id = "server"):
                yield Label("Server functionalities coming soon!")




class MainApp (App):

    CSS_PATH = "app.tcss"
    #define the shortcuts
    BINDINGS = [
            ("^q","quit", "Quit")
    ]

    def action_quit(self) -> None:
        self.exit()


    def compose(self) -> ComposeResult:
        yield Footer()
        yield NameContainer()
        yield Body()

    def on_mount(self) ->None:
        self.theme = "dracula"

        #on start bring the cursor focus to input widget
        self.user_prompt = self.query_one("#userprompt", Input)
        self.user_prompt.focus()


if __name__ == "__main__":
    app = MainApp()
    app.run()
