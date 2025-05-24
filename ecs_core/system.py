class System:

    def __init__(self):
        self.scene = None

    def update(self, dt: float):
        """
        Process game logic for one frame.
        dt: delta time in seconds since the last frame.
        """
        raise NotImplementedError