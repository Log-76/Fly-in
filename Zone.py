class Zone():
    def __init__(self, name: str, x: int, y: int, zone: str,
                 max_drone: int, color=None) -> None:
        """init for data for zone"""
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.zone = zone
        self.max_drone = max_drone
        self.drone_current = []

