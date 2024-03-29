import os
from datetime import datetime
from textual.app import App, ComposeResult, Binding
from textual.containers import Content
from textual.widgets import Input, Static, TextLog

start_header = "---begin---"


def make_line(timestamp: datetime, text: str) -> str:
    """Format a single line."""
    return "{}> {}".format(str(timestamp.ctime()), text)


def make_text(arr: list) -> str:
    return "\n".join([s.text for s in arr])


def make_filename(token: str) -> str:
    """Return a valid filename"""
    path = os.path.join(os.path.curdir, str(token).replace(':', '_') + ".log")
    return path


class ThinkTypeApp(App):

    CSS_PATH = "thinktype.css"

    BINDINGS = {
        Binding("ctrl+q", "quit", "Quit", show=False, priority=True),
    }

    def __init__(self):
        super(ThinkTypeApp, self).__init__()

    def compose(self) -> ComposeResult:
        yield Content(TextLog(id="log"), id="log-container")
        yield Input(placeholder="Type your thoughts here")

    def on_mount(self) -> None:
        self.query_one(Input).focus()
        now = datetime.now()
        self.query_one("#log").write(make_line(now, start_header))

    def _handle_save(self, msg):
        try:
            cmd, fname = msg.value.split()
        except ValueError:
            log = self.query_one("#log")
            log.write(f"/s <filename>")
            return
        self._save_to_file(fname)

    def _handle_quit(self, msg=None):
        self.exit()

    def on_input_submitted(self, message: Input.Submitted) -> None:
        if message.value:
            self.query_one("#log").write(
                make_line(datetime.now(), message.value))
            self.query_one(Input).value = ""

            switch = {
                "/s": self._handle_save,
                "/q": self._handle_quit,
            }
            for k, v in switch.items():
                if message.value.startswith(k):
                    if callable(v):
                        v(message)

    def key_ctrl_s(self) -> None:
        now = datetime.now()
        fname = make_filename(now)
        self._save_to_file(fname)

    def _save_to_file(self, fname):
        log = self.query_one("#log")
        log.write(f"Saving to {fname}")
        with open(fname, 'a') as f:
            f.write(make_text(log.lines))


if __name__ == "__main__":
    app = ThinkTypeApp()
    app.run()