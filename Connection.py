from Zone import Zone


class Connexion():
    def __init__(self, hub_a: Zone, hub_b: Zone, meta: dict) -> None:
        """gestionaire des connexion"""
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.maxlink = meta.get("max_link_capacity", 1) if meta else 1
        self.current_drones = 0
        self.hub_a.add_neighbor(self.hub_b, self)
        self.hub_b.add_neighbor(self.hub_a, self)
