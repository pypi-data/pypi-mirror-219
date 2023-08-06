from dataclasses import dataclass

from catt.error import CastError
from textual import on
from textual.app import DEFAULT_COLORS
from textual.containers import Container
from textual.events import Key
from textual.widgets import Button
from textual.widgets import Static


@dataclass
class ControlsConfig:
    ffwd_secs: int = 30
    rewind_secs: int = 10
    vol_step: float = 0.1
    fancy_icons: bool = False


class LolCattControls(Static):
    CONTROLS = {
        'play_pause': '',
        'stop': '',
        'previous': '',
        'rewind': '',
        'ffwd': '',
        'next': '',
        'vol_down': '',
        'vol_up': '',
    }

    CONTROLS_ASCII = {
        'play_pause': 'Play/Pause',
        'stop': 'Stop',
        'previous': '|<',
        'rewind': '<<',
        'ffwd': '>>',
        'next': '>|',
        'vol_down': 'Vol-',
        'vol_up': 'Vol+',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config = ControlsConfig(
            fancy_icons=self.app.config['options'].get('fancy_icons', False)
        )
        self._pp_button_colors = [DEFAULT_COLORS['dark'].success, DEFAULT_COLORS['dark'].warning]
        self._pp_button = Button(self._get_control_label('play_pause'), id='play_pause_button')
        self._pp_button.styles.border_bottom = ('tall', self._pp_button_colors[0])
        self._stop_button = Button(self._get_control_label('stop'), id='stop_button')

    def _get_control_label(self, control: str) -> str:
        if self._config.fancy_icons:
            return self.CONTROLS[control]
        else:
            return self.CONTROLS_ASCII[control]

    def compose(self):
        with Container(id='controls'):
            with Container(id='playback_buttons'):
                yield self._pp_button
                yield self._stop_button

            with Container(id='wind_buttons'):
                yield Button(self._get_control_label('previous'), id='prev_button')
                yield Button(self._get_control_label('rewind'), id='rewind_button')
                yield Button(self._get_control_label('ffwd'), id='ffwd_button')
                yield Button(self._get_control_label('next'), id='next_button')

            with Container(id='volume_buttons'):
                yield Button(self._get_control_label('vol_down'), id='vol_down_button')
                yield Button(self._get_control_label('vol_up'), id='vol_up_button')

    @on(Button.Pressed, "#play_pause_button")
    def toggle_play_pause(self):
        try:
            self.app.caster.get_device().controller.play_toggle()
            self._pp_button.styles.border_bottom = ('tall', self._pp_button_colors[-1])
            self._pp_button_colors.reverse()
        except ValueError:
            pass

    @on(Button.Pressed, "#stop_button")
    def stop(self):
        if self.app.caster.get_cast_state().cast_info.get('player_state') in ['PLAYING', 'PAUSED']:
            self.app.caster.stop_cast()
        else:
            self.app.exit()

    @on(Button.Pressed, "#vol_down_button")
    def vol_down(self):
        self.app.caster.get_device().volumedown(self._config.vol_step)

    @on(Button.Pressed, "#vol_up_button")
    def vol_up(self):
        self.app.caster.get_device().volumeup(self._config.vol_step)

    @on(Button.Pressed, "#ffwd_button")
    def ffwd(self):
        try:
            self.app.caster.get_device().ffwd(self._config.ffwd_secs)
        except CastError:
            pass

    @on(Button.Pressed, "#rewind_button")
    def rewind(self):
        try:
            self.app.caster.get_device().rewind(self._config.rewind_secs)
        except CastError:
            pass

    @on(Button.Pressed, '#next_button')
    def next(self):
        try:
            self.app.caster.cast_next()
        except CastError:
            pass

    @on(Button.Pressed, '#prev_button')
    def prev(self):
        try:
            self.app.caster.cast_previous()
        except CastError:
            pass

    def on_key(self, event: Key) -> None:
        if event.key == 'space':
            self.toggle_play_pause()
        elif event.key == ('q'):
            self.app.exit()
        elif event.key in ('h', 'left'):
            self.rewind()
        elif event.key in ('l', 'right'):
            self.ffwd()
        elif event.key in ('j', 'down'):
            self.next()
        elif event.key in ('k', 'up'):
            self.prev()
        elif event.key == 'plus':
            self.vol_up()
        elif event.key == 'minus':
            self.vol_down()
        else:
            pass
