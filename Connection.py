from Zone import Zone


class Connexion():
    def __init__(self, hub_a: Zone, hub_b: Zone, meta) -> None:
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.meta = meta
