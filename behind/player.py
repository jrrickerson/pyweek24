import sge
from sge.gfx import Sprite, Color

from . import config
from . import objects

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
        self.jump_speed = config.PLAYER_JUMP_VELOCITY
        self.controls = config.PLAYER_CONTROLS
        self.empty_sprite = empty_sprite()
        self.load_sprites(image_dict)
        self.direction = 1
        self.state = 'idle'
        self.on_platform = None

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

    def walk(self, time_passed):
        room_right_wall = sge.game.current_room.width
        room_left_wall = 0

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

    def jump(self):
        self.state = 'jumping'
        self.yvelocity = self.jump_speed
        self.yacceleration = config.GRAVITY

    def fall(self):
        self.state = 'jumping'
        self.yacceleration = config.GRAVITY
        self.image_index = 3

    def land(self, surface_level):
        self.yacceleration = 0
        self.yvelocity = 0
        self.image_bottom = surface_level
        self.state = 'idle'

    def set_state(self):
        if self.state == 'jumping':
            # If we were jumping and we didn't hit a platform,
            # stop at the floor
            if self.image_bottom >= sge.game.current_room.floor:
                self.land(sge.game.current_room.floor)
                self.on_platform = None
        else:
            self.state = 'walking' if self.xvelocity else 'idle'
            if self.on_platform:
                if (self.x < self.on_platform.bbox_left or
                        self.x > self.on_platform.bbox_right):
                    self.on_platform = None
                    self.fall()

    def event_step(self, time_passed, delta_multi):
        self.walk(time_passed)
        self.set_state()

    def event_key_press(self, key, _):
        if key in self.controls['jump']:
            if (self.image_bottom >= sge.game.current_room.floor or
                    self.on_platform):
                self.jump()

    def event_collision(self, other, xdirection, ydirection):
        if isinstance(other, objects.Platform):
            # Hit side of platform
            if xdirection:
                print('Hit side')
                self.xvelocity = 0
            # Hit platform above - stop moving up
            if ydirection == -1:
                print('Bumped')
                self.yvelocity = 0
            # Landed on platform - stop falling
            if ydirection == 1:
                print('Landed')
                self.land(other.bbox_top)
                self.on_platform = other
