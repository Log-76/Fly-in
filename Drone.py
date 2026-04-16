from Zone import Zone
import heapq


class Drone():
    def __init__(self, id: str, hub: Zone, target: Zone) -> None:
        """declaration des variable de la classe"""
        self.id = id
        self.hub: Zone = hub
        self.target = target
        self.stuck = 0
        self.index = 0
        self.total_cost = 0
        self.couldown = 0
        self.path: list[Zone] = []
        self.stock = {"normal": 1, "restricted": 2, "priority": 1}
        self.couldown_bool = False

    def move(self) -> str | None:
        """deplacement"""
        if self.target != self.hub:
            if self.couldown == 0:
                if self.index < len(self.path):
                    temp = self.path[self.index]
                    connection = None
                    for neighbor, link in self.hub.adjacent:
                        if neighbor == temp:
                            connection = link
                            break
                    if temp.can_enter() and (connection is None
                                             or connection.current_drones <
                                             int(connection.maxlink)):
                        if (temp.can_enter() is True and
                                temp.zone == "restricted" and
                                self.couldown_bool is False):
                            self.couldown += 1
                            self.index += 1
                            return f"D{self.id}-{self.hub.name}->{temp.name}"
                        elif (temp.can_enter() is True or
                              self.couldown_bool is True):
                            if self.couldown_bool and connection:
                                connection.current_drones -= 1
                            self.couldown_bool = False
                            self.total_cost += self.stock[temp.zone]
                            self.hub.drone_current.remove(self.id)
                            self.hub = temp
                            self.hub.drone_current.append(self.id)
                            self.index += 1
                            return f"D{self.id}-{self.hub.name}"
            else:
                self.couldown -= 1
                if self.couldown == 0:
                    self.couldown_bool = True
                    return self.move()
                return None

    def compute_path(self) -> None:
        """chemin de resolution avec difshrack"""
        if self.hub == self.target:
            self.path = []
            return
        # 1. File de priorité : (coût_cumulé, zone_actuelle)
        queu = [(0, 0, self.hub)]
        # 2. Suivi des coûts et des parents
        costs = {self.hub: 0}
        parents = {self.hub: None}
        while queu:
            # Récupère la zone avec le coût le plus faible
            current_cost, _, current_zone = heapq.heappop(queu)
            # Si on a trouvé la destination, on arrête l'exploration
            if current_zone == self.target:
                break

            # Sinon, on regarde les voisins
            for neighbor, link in current_zone.adjacent:
                if neighbor.zone == "blocked":
                    continue

                # --- CALCUL DU POIDS STRATÉGIQUE ---
                # Restricted = 2 tours, Normal = 1 tour
                weigth = self.stock.get(neighbor.zone, 1)

                # Bonus pour les zones priority
                # (on réduit virtuellement le coût)
                if neighbor.zone == "priority":
                    weigth = 0.1
                if link.current_drones >= int(link.maxlink):
                    link_penalty = 3.0
                else:
                    link_penalty = 0
                new_cost = (current_cost + weigth + link_penalty +
                            (len(neighbor.drone_current) /
                             neighbor.max_drone) * 0.9)

                # Si on trouve un chemin moins coûteux vers ce voisin
                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    parents[neighbor] = current_zone
                    heapq.heappush(queu, (new_cost, id(neighbor), neighbor))

        if self.target not in parents:
            self.path = []
            return

        path = []
        current = self.target
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        self.path = path[1:]
