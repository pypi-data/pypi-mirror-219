from typing import Dict

from textual.app import App
from textual.containers import Container
from textual.screen import Screen

from lolcatt.casting.caster import Caster
from lolcatt.ui.lolcatt_controls import LolCattControls
from lolcatt.ui.lolcatt_device_info import LolCattDeviceInfo
from lolcatt.ui.lolcatt_playback_info import LolCattPlaybackInfo
from lolcatt.ui.lolcatt_progress import LolCattProgress
from lolcatt.ui.lolcatt_url_input import LolCattUrlInput


class RemoteScreen(Screen):
    """A screen for the remote control UI."""

    def compose(self):
        yield Container(
            LolCattDeviceInfo(),
            LolCattPlaybackInfo(),
            LolCattProgress(),
            LolCattControls(),
            LolCattUrlInput(),
            id='app',
        )


class LolCatt(App):
    """The main application class for lolcatt."""

    CSS_PATH = 'ui/lolcatt.css'

    def __init__(self, device_name: str = None, config: Dict = None, *args, **kwargs):
        self.config = config
        self.caster = Caster(device_name, config=config)
        self.remote_screen = None
        super().__init__(*args, **kwargs)

    def on_mount(self):
        self.remote_screen = RemoteScreen()
        self.install_screen(self.remote_screen, name='remote')
        self.push_screen('remote')


if __name__ == '__main__':
    app = LolCatt('default')
    app.run()
