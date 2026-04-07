import Zone
import random


class Drone():
    def __init__(self, id: str, hub: Zone, target: Zone):
        self.id = id
        self.hub: Zone = hub
        self.target = target
        self.path: list[Zone] = []

    def move(self) -> None:
        if self.target != self.hub:
            self.path.append(self.hub)
            temp = random(self.hub.adjacent)
            if temp.can_enter() is True:
                self.hub.drone_current.pop()
                self.hub = temp
                self.hub.drone_current.append(self.id)
