import sge

from . import config
from . import game
from . import player
from . import background
from . import rooms


def initialize(config):
    """Load assets and initialize the game objects"""
    sge.game = game.Game(
        width=config.GAME_WINDOW_WIDTH,
        height=config.GAME_WINDOW_HEIGHT,
        fps=config.GAME_FPS,
        window_text=config.GAME_WINDOW_TITLE)

    # there are two sides, 'front' and 'behind'
    bg_obj = background.Background('front')

    player_obj = player.Player(
        config.PLAYER_SPRITES,
        sge.game.width / 2,
        rooms.ScrollableLevel.floor - player.Player.HEIGHT,
    )
    sge.game.start_room = rooms.ScrollableLevel(
        player=player_obj, width=10000, background=bg_obj, ruler=True)
    sge.game.mouse_visible = False

def run():
    """Start the game running"""
    sge.game.start()


if __name__ == '__main__':
    initialize(config)
    run()
