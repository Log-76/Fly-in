from Zone import Zone
from collections import deque


class Drone():
    def __init__(self, id: str, hub: Zone, target: Zone) -> None:
        """declaration des variable de la classe"""
        self.id = id
        self.hub: Zone = hub
        self.target = target
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
                    if (temp.can_enter() is True and
                            temp.zone == "restricted" and
                            self.couldown_bool is False):
                        self.couldown += 1
                        self.index += 1
                        return f"D{self.id}-{self.hub.name}->{temp.name}"
                    elif (temp.can_enter() is True or
                          self.couldown_bool is True):
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
        """chemin de resolution avec BFS"""
        # 1. On met le point de départ dans la file
        queu = deque([self.hub])
        # 2. On garde trace des zones visitées pour éviter les boucles
        # et pour reconstruire le chemin {enfant: parent}
        visited = {self.hub: None}
        while queu:
            # On récupère la zone la plus ancienne ajoutée (popleft)
            current_zone = queu.popleft()
            # Si on a trouvé la destination, on arrête l'exploration
            if current_zone == self.target:
                break

            # Sinon, on regarde les voisins
            for neighbor in current_zone.adjacent:
                if neighbor not in visited and neighbor.zone != "blocked":
                    visited[neighbor] = current_zone
                    queu.append(neighbor)

        if self.target not in visited:
            self.path = []
            return

        path = []
        current = self.target
        while current is not None:
            path.append(current)
            current = visited[current]
        path.reverse()
        self.path = path[1:]
