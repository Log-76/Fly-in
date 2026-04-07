import Zone


class Drone():
    def __init__(self, id: str, hub: Zone, target: Zone):
        self.id = id
        self.hub = hub
        self.target = target
        self.path: list[Zone] = []
    
    def move(self) -> None:
