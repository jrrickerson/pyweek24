import sge
from sge.gfx import Sprite, Color


class ScrollableLevel(sge.dsp.Room):
    def __init__(self, *args, player=None, ruler=False, **kwargs):
        self.player = player
        self.MOVE_PER_SEC = 200
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

    def scroll_view(self, time_passed):
        moved = (time_passed / 1000) * self.MOVE_PER_SEC
        pressed = sge.keyboard.get_pressed

        y_dir = 0
        #if pressed('up') or pressed('w'):
        #    y_dir = -1.0
        #if pressed('down') or pressed('s'):
        #    y_dir = 1.0

        x_dir = 0
        if pressed('right') or pressed('d'):
            x_dir += 1.0
        if pressed('left') or pressed('a'):
            x_dir += -1.0

        self.player.x += (x_dir * moved)
        self.player.y += (y_dir * moved)
        self.views[0].x += (x_dir * moved)
        self.views[0].y += (y_dir * moved)

    def event_step(self, time_passed, delta_multi):
        self.scroll_view(time_passed)
