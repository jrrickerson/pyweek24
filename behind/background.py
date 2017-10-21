import sge
from sge.gfx import Sprite, Color

from . import config


class Background(sge.gfx.Background):
    # setup scolling background image
    def __init__(self, state_name):
        self.state_name = state_name
        scroll_level = config.BACKGROUND_SPRITES[self.state_name]
        sprite_lev_1 = sge.gfx.Sprite(scroll_level['name'], scroll_level['directory'])
        background_layer = sge.gfx.BackgroundLayer(sprite_lev_1, 0, 0)
        self.layers = [background_layer]
        self.color = sge.gfx.Color("black")
