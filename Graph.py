from Zone import Zone
from Connection import Connexion
from Drone import Drone


class Graph():
    def __init__(self, data: dict) -> None:
        """stock of element"""
        self.total_cost = 0
        self.energie_cost = 0
        self.data = data
        self.hub: dict = {}
        self.connexion: list[Connexion] = []
        self.drones: list[Drone] = []

    def load_hub(self) -> None:
        """this fonction create all hub need"""
        for temps in self.data["hub"]:
            self.hub[temps[0]] = Zone(*temps)

    def load_connex(self) -> None:
        """this fonction create all connexion in data"""
        for temps in self.data["connexion"]:
            self.connexion.append(Connexion(self.hub[temps[0]],
                                            self.hub[temps[1]], temps[2]))

    def load_drones(self) -> None:
        """this fonction create all drone need"""
        for temps in range(self.data["drone"]):
            self.drones.append(Drone(temps, self.hub[self.data["start_hub"]],
                                     self.hub[self.data["end_hub"]]))

    def setup(self) -> None:
        """this metho activate all fonction"""
        self.load_hub()
        self.load_connex()
        self.load_drones()
        for drone in self.drones:
            drone.compute_path()

    def run(self) -> None:
        """run graph"""
        self.setup()
        while any(drone.hub != drone.target for drone in self.drones):
            for drone in self.drones:
                drone.move()
            self.total_cost += 1
        for drone in self.drones:
            self.energie_cost += drone.total_cost
