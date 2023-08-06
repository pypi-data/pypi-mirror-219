from dataclasses import dataclass
from typing import ClassVar

from textual import on
from textual.binding import Binding
from textual.binding import BindingType
from textual.containers import Container
from textual.events import Key
from textual.widgets import Input
from textual.widgets import Static


class InputField(Input):
    @dataclass
    class Enqueued(Input.Submitted):
        pass

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding('left', 'cursor_left', 'cursor left', show=False),
        Binding('ctrl+left', 'cursor_left_word', 'cursor left word', show=False),
        Binding('right', 'cursor_right', 'cursor right', show=False),
        Binding('ctrl+right', 'cursor_right_word', 'cursor right word', show=False),
        Binding('backspace', 'delete_left', 'delete left', show=False),
        Binding('home,ctrl+a', 'home', 'home', show=False),
        Binding('end,ctrl+e', 'end', 'end', show=False),
        Binding('delete,ctrl+d', 'delete_right', 'delete right', show=False),
        Binding('enter', 'submit', 'submit', show=False),
        Binding('ctrl+w', 'delete_left_word', 'delete left to start of word', show=False),
        Binding('ctrl+u', 'delete_left_all', 'delete all to the left', show=False),
        Binding('ctrl+f', 'delete_right_word', 'delete right to start of word', show=False),
        Binding('ctrl+k', 'delete_right_all', 'delete all to the right', show=False),
        Binding('ctrl+s', 'enqueue', 'submit to the playback queue', show=False),
    ]

    async def action_enqueue(self) -> None:
        """Handle an enqueue action.

        Normally triggered by the user pressing Ctrl+s. This will also run any validators.
        """
        print('enqueue')
        validation_result = self.validate(self.value)
        self.post_message(self.Enqueued(self, self.value, validation_result))


class LolCattUrlInput(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input = InputField(id='url_input', placeholder='Enter URL or path to cast...')
        self._input.cursor_blink = False

    @on(InputField.Submitted, '#url_input')
    def cast_url(self):
        if self._input.value == '':
            return
        if self._input.value:
            self.app.caster.enqueue(self._input.value, front=True)
            self._input.value = ''
            self.app.caster.cast_next()

    @on(InputField.Enqueued, '#url_input')
    def enqueue_url(self):
        if self._input.value == '':
            return
        if self._input.value:
            self.app.caster.enqueue(self._input.value, front=True)
            self._input.value = ''

    def compose(self):
        yield Container(self._input, id='url_input_container')

    def on_key(self, event: Key):
        if event.key == 'escape':
            self.app.remote_screen.focus_next()

    def on_mount(self):
        self._input.focus()
