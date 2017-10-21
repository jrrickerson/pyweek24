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
    # These are mostly used for choosing the animation.
    STATES = (
        'idle',
        'walking',
        'jumping',
        'damaged',
        'killed',
        'dead',
    )
    # This needs to be the same as the sprite height.
    HEIGHT = 64

    def __init__(self, image_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = None
        self.move_speed = config.PLAYER_MOVE_SPEED
        self.controls = config.PLAYER_CONTROLS
        self.empty_sprite = empty_sprite()
        self.load_sprites(image_dict)
        self.direction = 1
        self.state = 'idle'

    def load_sprites(self, image_dict):
        self.sprite_dict = {}
        for s in self.STATES:
            sprite_params = image_dict.get(s, None)
            if sprite_params and sprite_params['name']:
                sprite = Sprite(**sprite_params)
                print('Loaded sprite {}, {} frames'.format(
                    sprite.name, sprite.frames))
                self.sprite_dict[s] = sprite
        # Generate reverse versions of sprites
        mirror_sprites = {}
        for state in self.sprite_dict:
            s = self.sprite_dict[state].copy()
            s.mirror()
            print('Loaded sprite {}, {} frames'.format(
                s.name, s.frames))
            mirror_sprites[state + '_mirror'] = s
        self.sprite_dict.update(mirror_sprites)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        assert new_state in self.STATES
        if self._state != new_state:
            print('Player state changed to {}'.format(new_state))
            self._state = new_state
            self.event_state_changed(new_state)

    def event_state_changed(self, new_state):
        if self.direction == -1:
            self.sprite = self.sprite_dict.get(
                self.state + '_mirror', self.empty_sprite)
            # Set to None to use the Sprite's FPS
            # This won't be updated if we don't set it here
            self.image_fps = None
        else:
            self.sprite = self.sprite_dict.get(
                self.state, self.empty_sprite)
            # Set to None to use the Sprite's FPS
            # This won't be updated if we don't set it here
            self.image_fps = None

    def _control_pressed(self, control_name):
        """Return True if any of the keys mapped to the control_name is
        being pressed"""
        return any([sge.keyboard.get_pressed(k) for k in
                   self.controls.get(control_name, tuple())])

    def event_step(self, time_passed, delta_multi):
        room_right_wall = sge.game.current_room.width
        room_left_wall = 0
        # Scroll with player movement.  Keep the player in center of the
        # screen, except at the start and end of the level
        self.xvelocity = 0
        if self._control_pressed('right'):
            self.xvelocity += 1
        if self._control_pressed('left'):
            self.xvelocity -= 1
        self.xvelocity *= self.move_speed * time_passed / 1000

        if self.xvelocity < 0:
            self.direction = -1
        elif self.xvelocity > 0:
            self.direction = 1


        # The following code could be generalized as collision detection.
        # Limit to the confines of the current room
        if self.image_left <= room_left_wall and self.xvelocity < 0:
            self.xvelocity = 0
        if self.image_right >= room_right_wall and self.xvelocity > 0:
            self.xvelocity = 0

        if self.image_bottom < sge.game.current_room.floor:
            self.yacceleration = config.GRAVITY
            self.state = 'jumping'
        else:
            self.image_bottom = sge.game.current_room.floor
            self.yacceleration = 0
            # Started walking this frame
            self.state = 'walking' if self.xvelocity else 'idle'

    def event_key_press(self, key, _):
        if (self.image_bottom >= sge.game.current_room.floor
            and key in self.controls['jump']):
            self.yvelocity = -30
