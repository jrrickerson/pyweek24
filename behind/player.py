import sge
from sge.gfx import Sprite, Color

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
