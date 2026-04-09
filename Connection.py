from Zone import Zone


class Connexion():
    def __init__(self, hub_a: Zone, hub_b: Zone, meta: dict = None) -> None:
        """gestionaire des connexion"""
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.meta = meta
        self.hub_a.add_neighbor(self.hub_b)
        self.hub_b.add_neighbor(self.hub_a)
