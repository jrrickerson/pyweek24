import sge

from . import config
from . import game
from . import player
from . import background
from . import rooms
from . import objects


def initialize(config):
    """Load assets and initialize the game objects"""
    sge.game = game.Game(
        width=config.GAME_WINDOW_WIDTH,
        height=config.GAME_WINDOW_HEIGHT,
        fps=config.GAME_FPS,
        window_text=config.GAME_WINDOW_TITLE)

    platform_left = sge.gfx.Sprite(**config.PLATFORM_SPRITES['left'])
    platform_right = sge.gfx.Sprite(**config.PLATFORM_SPRITES['right'])
    platform_middle = sge.gfx.Sprite(**config.PLATFORM_SPRITES['middle'])

    # there are two sides, 'front' and 'behind'
    bg_obj = background.Background('front')

    player_obj = player.Player(
        config.PLAYER_SPRITES,
        sge.game.width / 2,
        rooms.ScrollableLevel.floor - player.Player.HEIGHT,
    )
    test_platforms = [
        (500, sge.game.height / 3 * 2, 16 * 10, 16),
        (700, sge.game.height / 2, 16 * 20, 16),
        (1500, sge.game.height / 4 * 3, 16 * 3, 16),
        (1700, sge.game.height / 3 * 2, 16 * 6, 16),
    ]
    platforms = [objects.Platform(
        x, y, w, h,
        left_sprite=platform_left, middle_sprite=platform_middle,
        right_sprite=platform_right) for x, y, w, h in test_platforms]

    sge.game.start_room = rooms.ScrollableLevel(
        objects=platforms,
        player=player_obj, width=10000, background=bg_obj, ruler=False)
    sge.game.mouse_visible = False

def run():
    """Start the game running"""
    sge.game.start()


if __name__ == '__main__':
    initialize(config)
    run()
