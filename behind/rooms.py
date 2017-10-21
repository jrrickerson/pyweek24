import sge
from sge.gfx import Sprite, Color

from . import config


class ScrollableLevel(sge.dsp.Room):
    def __init__(self, *args, player=None, ruler=False, **kwargs):
        self.scroll_speed = config.PLAYER_MOVE_SPEED
        self.controls = config.PLAYER_CONTROLS

        self.player = player

        super().__init__(*args, **kwargs)
        self.add(player)

        if ruler:
            self.add_ruler()

    def add_ruler(self):
        self.ruler = []
        font = sge.gfx.Font(size=20)
        for x in range(0, self.width, 100):
            mark_text = Sprite(name=None, width=100, height=100)
            mark_text.draw_text(
                font, '{}'.format(x), 0, 0,
                color=sge.gfx.Color("red"),
                halign="center", valign="middle")
            mark = sge.dsp.Object(
                x, self.height - 100, sprite=mark_text, tangible=False)
            self.ruler.append(mark)
            self.add(mark)

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

    def event_step(self, time_passed, delta_multi):
        self.scroll_view(time_passed)
