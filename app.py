from libagent import get_commands
import asyncio 
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Static, TabbedContent, TabPane, Label, Input
from textual.containers import Container, Vertical, VerticalScroll


class NameContainer(Container):
    #ASCII Art container

    def compose(self) -> ComposeResult:
        yield Static(
            r'''
▗▖  ▗▖ ▗▄▖  ▗▄▖  ▗▄▄▖▗▄▄▄▖
▐▛▚▞▜▌▐▌ ▐▌▐▌ ▐▌▐▌     █  
▐▌  ▐▌▐▌ ▐▌▐▛▀▜▌ ▝▀▚▖  █  
▐▌  ▐▌▝▚▄▞▘▐▌ ▐▌▗▄▄▞▘  █ 
''',id = "ascii"
        )


class UserPrompt(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Input(
                placeholder = "Give your instruction here",
                id = "userprompt"
        )

    @on (Input.Submitted)
    async def send_user_input(self) -> None:
        input = self.query_one(Input)
        user_input = input.value
        input.value = ""                                        #clear for nxt input

        label = Label("Instruction sent !", id ="sent-msg")
        self.mount(label)
        label.styles.animate("opacity", value=0, duration=1.5)    #fadeout animation

        response = get_commands(user_input = user_input, model = 'llama3.2')
        command = Label(response['response'], id ="command")
        self.mount(command)
        await asyncio.sleep(2.5)  #give enough time for animation before the label is removed
        label.remove()




class Body(Vertical):
    # main body container of the app

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Terminal", id = "terminal"):
                yield UserPrompt()

            with TabPane("Server", id = "server"):
                yield Label("Server functionalities coming soon!")




class MainApp (App):

    CSS_PATH = "app.tcss"

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
