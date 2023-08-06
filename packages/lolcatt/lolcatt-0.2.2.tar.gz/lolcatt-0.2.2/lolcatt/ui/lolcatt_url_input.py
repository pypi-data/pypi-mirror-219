from textual import on
from textual.containers import Container
from textual.events import Key
from textual.widgets import Input
from textual.widgets import Static


class LolCattUrlInput(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input = Input(id='url_input', placeholder='Enter URL to cast...')
        self._input.cursor_blink = False

    @on(Input.Submitted, "#url_input")
    def cast_url(self):
        if self._input.value == '':
            return
        if self._input.value:
            self.app.caster.enqueue(self._input.value, front=True)
            print(self.app.caster._queue)
            self.app.caster.cast_next()
            self._input.value = ''

    def compose(self):
        yield Container(self._input, id='url_input_container')

    def on_key(self, event: Key):
        if event.key == 'escape':
            self.app.remote_screen.focus_next()

    def on_mount(self):
        self._input.focus()
