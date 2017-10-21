import math
import sge
from sge.gfx import Sprite, Color

from . import config


class ScrollableLevel(sge.dsp.Room):
    # This is currently just a number, but it could be expanded to some kind of
    # platform object.
    floor = config.GAME_WINDOW_HEIGHT * 8 // 10

    def __init__(self, *args, player=None, ruler=False, **kwargs):
        self.scroll_speed = config.PLAYER_MOVE_SPEED
        self.controls = config.PLAYER_CONTROLS
        self.ruler = ruler
        self.player = player

        super().__init__(*args, **kwargs)
        self.add(player)

    def show_ruler(self):
        font = sge.gfx.Font(size=20)
        view = self.views[0]
        first_mark = int(math.floor(view.x / 100)) * 100
        last_mark = int(math.ceil((view.x + view.width) / 100)) * 100
        for x in range(first_mark, last_mark, 100):
            self.project_text(
                font, '{}'.format(x),
                x, self.height - 50, 0,
                color=sge.gfx.Color("red"),
                halign="center", valign="middle")

    def _control_pressed(self, control_name):
        """Return True if any of the keys mapped to the control_name is
        being pressed"""
        return any([sge.keyboard.get_pressed(k) for k in
                   self.controls.get(control_name, tuple())])

    def scroll_view(self, time_passed):
        moved = (time_passed / 1000) * self.scroll_speed
        view = self.views[0]
        view_center = view.x + view.width / 2

        y_dir = 0
        x_dir = 0
        if self._control_pressed('right') and self.player.x >= view_center:
            x_dir += 1.0
        if self._control_pressed('left') and self.player.x <= view_center:
            x_dir += -1.0

        self.views[0].x += (x_dir * moved)
        self.views[0].y += (y_dir * moved)

    def event_key_press(self, key, char):
        # Press R to toggle ruler
        # Capture this here so we only capture a single event,
        # not multiple across multiple frames
        if key == 'r':
            self.ruler = not self.ruler

    def event_step(self, time_passed, delta_multi):
        self.scroll_view(time_passed)

        if self.ruler:
            self.show_ruler()
