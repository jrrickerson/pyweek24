import sge
from sge.gfx import Sprite, Color

from . import config

NO_SPRITE = None


def empty_sprite():
    global NO_SPRITE
    if not NO_SPRITE:
        NO_SPRITE = Sprite(name=None)
        NO_SPRITE.draw_rectangle(
            0, 0, NO_SPRITE.width, NO_SPRITE.height, outline=Color('white'),
            fill=Color('blue'))
    return NO_SPRITE


class Player(sge.dsp.Object):
    STATES = (
        'idle',
        'walking',
        'jumping',
        'damaged',
        'killed',
        'dead',
    )

    def __init__(self, image_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_speed = config.PLAYER_MOVE_SPEED
        self.controls = config.PLAYER_CONTROLS
        self.empty_sprite = empty_sprite()
        self.load_sprites(image_dict)
        self.state = 'idle'

    def load_sprites(self, image_dict):
        self.sprite_dict = {}
        for s in self.STATES:
            sprite_params = image_dict.get(s, None)
            if sprite_params and sprite_params['name']:
                sprite = Sprite(**sprite_params)
                self.sprite_dict[s] = sprite

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        assert new_state in self.STATES
        self._state = new_state
        self.event_state_changed()

    def event_state_changed(self):
        print('Player state changed to {}'.format(self.state))
        self.sprite = self.sprite_dict.get(
            self.state, self.empty_sprite)

    def _control_pressed(self, control_name):
        """Return True if any of the keys mapped to the control_name is
        being pressed"""
        return any([sge.keyboard.get_pressed(k) for k in
                   self.controls.get(control_name, tuple())])

    def move(self, time_passed):
        moved = (time_passed / 1000) * self.move_speed
        x_dir = 0
        y_dir = 0
        room_right_wall = sge.game.current_room.width
        room_left_wall = 0
        # Scroll with player movement.  Keep the player in center of the
        # screen, except at the start and end of the level
        if self._control_pressed('right'):
            x_dir += 1.0
        if self._control_pressed('left'):
            x_dir += -1.0

        # Limit to the confines of the current room
        if self.image_left <= room_left_wall and x_dir < 0:
            x_dir = 0
        if self.image_right >= room_right_wall and x_dir > 0:
            x_dir = 0

        self.move_x(x_dir * moved)
        self.move_y(y_dir * moved)

    def event_step(self, time_passed, delta_multi):
        self.move(time_passed)
