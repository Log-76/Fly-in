from Zone import Zone
from collections import deque


class Drone():
    def __init__(self, id: str, hub: Zone, target: Zone):
        self.id = id
        self.hub: Zone = hub
        self.target = target
        self.index = 0
        self.path: list[Zone] = []

    def move(self) -> None:
        if self.target != self.hub:
            if self.index < len(self.path):
                temp = self.path[self.index]
                if temp.can_enter() is True:
                    self.hub.drone_current.remove(self.id)
                    self.hub = temp
                    self.hub.drone_current.append(self.id)
                    self.index += 1

    def compute_path(self) -> list[Zone]:
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

        path = []
        current = self.target
        while current is not None:
            path.append(current)
            current = visited[current]
        path.reverse()
        self.path = path
