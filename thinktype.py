import os
from datetime import datetime
from rich import print
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel


def make_line(timestamp: datetime, text: str) -> str:
    """Format a single line."""
    return "{} {}".format(str(timestamp), text)

def make_text(arr: list) -> str:
    """Format all of the lines into a Renderable"""
    return "\n".join(arr)

def make_filename(token: str) -> str:
    """Return a valid filename"""
    path = os.path.join(os.path.curdir, str(token).replace(':', '_') + ".log")
    return path

def make_layout() -> Layout:
    """Define the layout of the screen."""
    layout = Layout()
    layout.split_column(Layout(Panel([]), name="upper", size=None, ratio=90),
                        Layout(Panel([]), name="lower"))
    return layout

if __name__ == "__main__":
    quit = ['/quit', '/q']
    save = ['/save', '/s']
    now = datetime.now()
    thoughts = [make_line(now, 'start')]
    fname = make_filename(now) 
    layout = make_layout()

    console = Console()
    intext = None
    while intext not in quit:
        layout['upper'].update(Panel(make_text(thoughts)))
        print(layout)
        intext = console.input(prompt="[blink]> ").strip()
        now = datetime.now()
        if intext in save:
            with open(fname, 'a') as f:
                f.write(make_text(thoughts))
            intext = None
        if intext:
            thoughts.append(make_line(now, intext))
        
