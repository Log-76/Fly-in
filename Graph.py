from Zone import Zone
from Connection import Connexion
from Drone import Drone
from typing import Any


class Graph():
    def __init__(self, data: dict[Any, Any]) -> None:
        """stock of element"""
        self.total_cost = 0
        self.energie_cost = 0
        self.data = data
        self.hub: dict[Any, Any] = {}
        self.connexion: list[Connexion] = []
        self.drones: list[Drone] = []

    def load_hub(self) -> None:
        """this fonction create all hub need"""
        start = self.data["start_hub"][0]
        self.hub[start] = Zone(self.data["start_hub"][0],
                               self.data["start_hub"][1],
                               self.data["start_hub"][2],
                               self.data["start_hub"][3]["zone"],
                               self.data["start_hub"][3]["max_drones"],
                               self.data["start_hub"][3]["color"])
        for temps in self.data["hub"]:
            self.hub[temps[0]] = Zone(temps[0],
                                      temps[1],
                                      temps[2],
                                      temps[3]["zone"],
                                      temps[3]["max_drones"],
                                      temps[3]["color"])
        end = self.data["end_hub"][0]
        self.hub[end] = Zone(self.data["end_hub"][0],
                             self.data["end_hub"][1],
                             self.data["end_hub"][2],
                             self.data["end_hub"][3]["zone"],
                             self.data["end_hub"][3]["max_drones"],
                             self.data["end_hub"][3]["color"])

    def load_connex(self) -> None:
        """this fonction create all connexion in data"""
        for temps in self.data["connection"]:
            if isinstance(temps, tuple):
                # tuple contient une list donc pour voyager dedans [][]
                # naviguer dans tuple []
                hub_b, hub_a, meta = temps[0][0], temps[0][1], temps[1]
                self.connexion.append(Connexion(self.hub[hub_a],
                                                self.hub[hub_b], meta))
            else:
                hub_b, hub_a = temps[0], temps[1]
                self.connexion.append(Connexion(self.hub[hub_a],
                                                self.hub[hub_b], {}))

    def load_drones(self) -> None:
        """this fonction create all drone need"""
        for i in range(0, self.data["nb_drones"]):
            self.drones.append(Drone(str(i),
                                     self.hub[self.data["start_hub"][0]],
                                     self.hub[self.data["end_hub"][0]]))
        for drone in self.drones:
            drone.hub.drone_current.append(drone.id)

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
            move = []
            # On trie pour la priorité
            sorted_drones = sorted(self.drones,
                                   key=lambda d: (len(d.path), d.id))
            drones_trying_to_move = 0
            drones_blocked_this_turn = 0

            for drone in sorted_drones:
                if drone.hub != drone.target:
                    drones_trying_to_move += 1
                    res = drone.move()
                    if res:
                        move.append(res)
                        drone.stuck = 0
                    else:
                        # Recalcul après 2 tours de blocage
                        if drone.stuck >= 2:
                            drone.compute_path()
                            # Si après recalcul le chemin est vide
                            if not drone.path:
                                raise Exception(f"Drone {drone.id} has no "
                                                "possible path to target")
                        drone.stuck += 1
                        drones_blocked_this_turn += 1

            # SECURITÉ : Si tous les drones qui doivent bouger sont bloqués
            if (drones_trying_to_move > 0 and
                    drones_blocked_this_turn == drones_trying_to_move):
                raise Exception("Global Deadlock: No drones can move anymore")

            self.total_cost += 1
            if move:
                print(" ".join(move))
