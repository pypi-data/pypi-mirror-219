"""@ 

# app.py

**Author:** Conner Marzen

**Description:** ViewerApp class, which is the entrypoint for the documentation
viewer appliction.
@"""

import os

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import DirectoryTree, Footer, MarkdownViewer

from docwalker.parser import Parser

WELCOME_MESSAGE = """
# DocWalker

DocWalker is a simple, in-place documentation viewer. It takes advantage of
special comment symbols to read documentation right inside your source code.

## Getting Started

Press the **`O`** key to open the directory tree and select a document to view
its documentation.
"""


class ViewerApp(App):
    """@
    ## Class: ViewerApp
    @"""

    CSS_PATH = "styles/main.css"

    BINDINGS = [
        Binding(key="o", action="open_file", description="Open File"),
        Binding(key="t", action="toggle_dark", description="Toggle Light/Dark Mode"),
        Binding(key="q", action="quit", description="Quit"),
    ]

    def __init__(self, src_dir: str, config: dict, **kwargs):
        """@
        ### def __init__

        Initialization function.
        @"""
        self._show_directory = False
        self._src_dir = src_dir
        self._config = config
        self._parser = Parser(self._config)
        super().__init__(**kwargs)

    async def action_open_file(self):
        widget = self.query_one("#dir-viewer", DirectoryTree)
        widget.toggle_class("hidden")
        self.set_focus(widget)
        self._show_directory = not self._show_directory

    @on(DirectoryTree.FileSelected)
    async def on_selected_file(self, event: DirectoryTree.FileSelected):
        widget = self.query_one("#md-viewer", MarkdownViewer)
        if (path := os.path.abspath(event.path)).endswith(".md"):
            with open(path, "r") as file:
                widget.document.update(file.read())
        elif os.path.isfile(event.path):
            data = self._parser.parse(event.path)
            if len(data) == 0:
                widget.document.update(
                    "# No documentation.\n\nThis document doesn't contain any special comments to extract."
                )
            else:
                widget.document.update(data)

    def compose(self) -> ComposeResult:
        yield MarkdownViewer(id="md-viewer", markdown=WELCOME_MESSAGE)
        yield DirectoryTree(self._src_dir, id="dir-viewer", classes="hidden")
        yield Footer()
