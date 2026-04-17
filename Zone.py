from typing import Any


class Zone():
    def __init__(self, name: str, x: int, y: int, zone: str,
                 max_drone: int = 1, color: Any = None) -> None:
        """init for data for zone"""
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.zone = zone
        self.max_drone = max_drone
        self.drone_current: list[Any] = []
        self.adjacent: list[tuple[Any, Any]] = []

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
            "green": "\033[1;32m",
            "lime": "\033[38;5;118m",
            "blue": "\033[1;34m",
            "red": "\033[1;31m",
            "darkred": "\033[1;38;5;88m",
            "crimson": "\033[1;38;5;197m",
            "brown": "\033[0;33m",
            "violet": "\033[38;5;183m",
            "orange": "\033[38;5;208m",
            "maroon": "\033[38;5;52m",
            "gold": "\033[38;5;220m",
            "yellow": "\033[33m",
            "cyan": "\033[36m",
            "purple": "\033[38;5;129m",
            "magenta": "\033[35m",
            "reset": "\033[0m"
        }
        # On récupère le code couleur, sinon reset par défaut
        reset = colors["reset"]
        rainbow_name = ""
        if self.color == "rainbow":
            rainbow_codes = ["\033[31m", "\033[38;5;208m",
                             "\033[33m", "\033[32m",
                             "\033[34m", "\033[35m"]
            for i, char in enumerate(self.name):
                color = rainbow_codes[i % len(rainbow_codes)]
                rainbow_name += f"{color}{char}"
            return f"{rainbow_name}{reset}"
        color_code = colors.get(self.color, colors["reset"])
        return f"{color_code}{self.name}{reset}"
