import sge
from sge.gfx import Sprite, Color

from . import config


class Platform(sge.dsp.Object):
    def __init__(self, x, y, width, height, left_sprite=None,
                 right_sprite=None, middle_sprite=None, **kwargs):
        self.left_sprite = left_sprite
        self.right_sprite = right_sprite
        self.middle_sprite = middle_sprite or kwargs.pop('sprite')
        sprite = self.create_platform_sprite(width, height)
        super().__init__(x, y, sprite=sprite, **kwargs)
        self.checks_collisions = False

    def create_platform_sprite(self, width, height):
        """Draw a dynamically sized platform sprite from a left, middle, and
        right sprite."""
        # Create an invisible rectangle the size of the platform
        sprite = Sprite(name=None, width=width, height=height)
        offset = 0
        # Draw left end
        if self.left_sprite:
            sprite.draw_sprite(self.left_sprite, 0, offset, 0)
            offset = self.left_sprite.width
        # Tile middle sprite through the end of the platform
        if self.middle_sprite:
            for x in range(offset, width, self.middle_sprite.width):
                sprite.draw_sprite(self.middle_sprite, 0, x, 0)
            offset = x
        # Draw right end
        if self.right_sprite:
            sprite.draw_sprite(
                self.right_sprite, 0, width - self.right_sprite.width, 0)

        return sprite