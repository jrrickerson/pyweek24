import sge


class Game(sge.dsp.Game):
    """Basic game object - only offers a keypress to quit."""
    def event_key_press(self, key, char):
        if 'escape' == key:
            self.event_close()

    def event_close(self):
        self.end()

