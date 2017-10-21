import sge

from . import config
from . import game
from . import player
from . import rooms


def initialize(config):
    """Load assets and initialize the game objects"""
    sge.game = game.Game(
        width=config.GAME_WINDOW_WIDTH,
        height=config.GAME_WINDOW_HEIGHT,
        fps=config.GAME_FPS,
        window_text=config.GAME_WINDOW_TITLE)
    player_obj = player.Player(
        config.PLAYER_SPRITES,
        sge.game.width / 2,
        sge.game.height / 3 * 2)
    sge.game.start_room = rooms.ScrollableLevel(
        player=player_obj, width=2000, ruler=True)
    sge.game.mouse_visible = False


def run():
    """Start the game running"""
    sge.game.start()


if __name__ == '__main__':
    initialize(config)
    run()
