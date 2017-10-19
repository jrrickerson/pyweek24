import sge
from sge import keyboard
from sge.gfx import Background, Color, Sprite


class CheckGame(sge.dsp.Game):
    """Test Game object"""
    def event_key_press(self, key, char):
        if 'escape' == key:
            self.event_close()

    def event_close(self):
        self.end()


class CheckPlayer(sge.dsp.Object):
    MOVE_PER_SEC = 100

    def __init__(self, *args, width=None, height=None, **kwargs):
        # Make a basic filled rectangle sprite for the player
        default_sprite = Sprite(height=height, width=width)
        default_sprite.draw_rectangle(
            0, 0, width, height,
            fill=sge.gfx.Color('green'),
            outline=sge.gfx.Color('white'),
            outline_thickness=2)
        sprite = kwargs.pop('sprite', None) or default_sprite
        super().__init__(*args, sprite=sprite, **kwargs)

    def event_step(self, time_passed, delta_multi):
        moved = (time_passed / 1000) * self.MOVE_PER_SEC

        y_dir = 0
        if keyboard.get_pressed('up') or keyboard.get_pressed('w'):
            y_dir = -1.0
        if keyboard.get_pressed('down') or keyboard.get_pressed('s'):
            y_dir = 1.0

        x_dir = 0
        if keyboard.get_pressed('right') or keyboard.get_pressed('d'):
            x_dir += 1.0
        if keyboard.get_pressed('left') or keyboard.get_pressed('a'):
            x_dir += -1.0

        self.move_x(x_dir * moved)
        self.move_y(y_dir * moved)


class CheckRoom(sge.dsp.Room):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = sge.gfx.Font(size=36)

    def event_step(self, time_passed, delta_mult):
        sge.game.project_text(
            self.font, "SGE Engine Test", sge.game.width / 2,
            sge.game.height / 4, color=sge.gfx.Color("red"),
            halign="center", valign="middle")
        sge.game.project_text(
            self.font, "Move with arrow keys or WASD\nPress Esc to exit",
            sge.game.width / 2, sge.game.height / 4 + 50,
            color=sge.gfx.Color("red"),
            halign="center", valign="middle")


def check():
    """Run a basic test to ensure dependencies are installed correctly."""
    sge.game = CheckGame(
        width=1024, height=768, fps=60, window_text='SGE Test')
    bg = sge.gfx.Background([], sge.gfx.Color("black"))
    player = CheckPlayer(
        sge.game.width / 2, sge.game.height / 2, width=100, height=200)
    sge.game.start_room = CheckRoom(
        objects=[player], background=bg)
    sge.game.mouse_visible = False
    sge.game.start()


if __name__ == '__main__':
    check()
