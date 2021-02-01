from minions.base import Minion


class PunchingBag(Minion):
    """ A 0/100 minion used for test cases where a generic minion is needed
    """
    def __init__(self, **kwargs):
        super().__init__(name="PunchingBag",
                         rank=1,
                         base_attack=0,
                         base_defense=100,
                         **kwargs)
