from typing import Tuple

from catt.error import CastError
from textual.containers import Container
from textual.events import Click
from textual.reactive import reactive
from textual.widgets import Label
from textual.widgets import ProgressBar
from textual.widgets import Static


class LolCattProgress(Static):
    current = reactive(0)
    duration = reactive(0)
    percent_complete = reactive(0)

    @staticmethod
    def _extract_progress(cast_info: dict) -> Tuple[float, float, float]:
        current = cast_info.get('current_time', 0.0)
        duration = cast_info.get('duration', 0.0)
        percent_complete = current / duration * 100 if duration else 0.0
        return current, duration, percent_complete

    def _format_time(self, seconds: float) -> str:
        if seconds is None:
            return '--:--'
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f'{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}'
        return f'{minutes:02.0f}:{seconds:02.0f}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pb = ProgressBar(total=100, show_percentage=False, show_eta=False, id='progress_bar')
        self.pblabel = Label('', id='progress_label')
        self._needed_width = 16  # FIXME: learn CSS

    def update_progress(self) -> int:
        self.current, self.duration, self.percent_complete = self._extract_progress(
            self.app.caster.get_cast_state().cast_info
        )
        self.pb.update(progress=self.percent_complete)
        current_fmt = self._format_time(self.current)
        duration_fmt = self._format_time(self.duration)
        upd_str = f'({current_fmt}/{duration_fmt})'
        padding = ' ' * max(0, (self._needed_width - len(upd_str)))
        self.pblabel.update(f'{padding}{upd_str}')

    def on_mount(self):
        self.update_progress()
        self.set_interval(
            interval=self.app.caster.get_update_interval(), callback=self.update_progress
        )

    def on_click(self, event: Click):
        min_x, max_x = (
            self.pb.content_region.x,
            self.pb.content_region.x + self.pb.content_region.width,
        )
        click_x = min(max(event.screen_x, min_x), max_x)
        fraction = min(1, (click_x - min_x) / (max_x - min_x))
        duration = self.app.caster.get_cast_state().cast_info.get('duration', 0.0)
        try:
            self.app.caster.get_device().seek(duration * fraction)
        except CastError:
            pass

    def compose(self):
        yield Container(self.pb, self.pblabel, id='progress')
