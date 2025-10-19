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


if __name__ == "__main__":
    app = MainApp()
    app.run()
