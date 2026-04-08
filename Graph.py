from Zone import Zone
from Connection import Connexion
from Drone import Drone


class Graph():
    def __init__(self, data: dict) -> None:
        """stock of element"""
        self.data = data
        self.hub: dict = {}
        self.connexion: list[Connexion] = []
        self.drones: list[Drone] = []

    def load_hub(self) -> None:
        for temps in self.data["hub"]:
            self.hub[temps[0]] = Zone(*temps)

    def load_connex(self) -> None:
        for temps in self.data["connexion"]:
            self.connexion.append(Connexion(self.hub[temps[0]],
                                            self.hub[temps[1]], temps[2]))

    def load_drones(self) -> None:
        for temps in range(self.data["drone"]):
            self.drones.append(Drone(temps, self.hub[self.data["start_hub"]],
                                     self.hub[self.data["end_hub"]]))

