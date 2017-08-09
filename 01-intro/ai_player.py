class AIPlayer:
    def __init__(self, policy=None):
        self._policy = policy or AIPlayer.default_policy

    @staticmethod
    def default_policy():
        pass
