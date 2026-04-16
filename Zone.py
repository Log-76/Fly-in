from typing import Any


class Zone():
    def __init__(self, name: str, x: int, y: int, zone: str,
                 max_drone: int = 1, color=None) -> None:
        """init for data for zone"""
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.zone = zone
        self.max_drone = max_drone
        self.drone_current: list[Any] = []
        self.adjacent: list['Zone'] = []

    def is_full(self) -> bool:
        """verif if max_drone is true"""
        if self.max_drone == len(self.drone_current):
            return True
        return False

    def can_enter(self) -> bool:
        """verif if is_full is False or if zone is blocked"""
        if (self.name == "impossible_goal" or "goal" in self.name
                or "start" in self.name):
            return True
        if self.is_full() is True or self.zone == "blocked":
            return False
        return True

    def add_neighbor(self, neighbor: 'Zone', connexion: Any) -> None:
        """add neighbor"""
        self.adjacent.append((neighbor, connexion))

    def get_colored_name(self) -> str:
        """Retourne le nom de la zone avec les codes ANSI directement"""
        colors = {
            "green": "\033[32m",
            "blue": "\033[34m",
            "red": "\033[31m",
            "yellow": "\033[33m",
            "cyan": "\033[36m",
            "magenta": "\033[35m",
            "reset": "\033[0m"
        }
        # On récupère le code couleur, sinon reset par défaut
        color_code = colors.get(self.color, colors["reset"])
        reset = colors["reset"]

        return f"{color_code}{self.name}{reset}"
