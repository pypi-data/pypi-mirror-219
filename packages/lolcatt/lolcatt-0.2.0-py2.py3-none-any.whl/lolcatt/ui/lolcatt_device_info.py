from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Label
from textual.widgets import Static

from lolcatt.utils.utils import marquee


class LolCattDeviceInfo(Static):
    label_str = reactive('')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = Label('')
        self._marquee_gen = None

    def _get_device_info(self) -> str:
        info = self.app.caster.get_device_name()
        if info is not None:
            msg = f'Connected to: "{info}"'
        else:
            msg = 'Not connected to a device. Try "lolcatt --scan".'
        return msg

    def _update_label(self):
        self.label_str = self._get_device_info() + ' '
        self.label.update(next(self._marquee_gen))

    def watch_label_str(self, value):
        self._marquee_gen = marquee(value, self.size.width, 2)

    def on_resize(self, value):
        self._marquee_gen = marquee(self.label_str, self.size.width, 2)

    def on_mount(self):
        self._update_label()
        self.set_interval(
            interval=self.app.caster.get_update_interval(), callback=self._update_label
        )

    def compose(self):
        yield Container(self.label, id='device_info')
