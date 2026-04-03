class Parse():
    """Parse a drone map config file."""
    def __init__(self) -> None:
        """Initialize the parser with an empty data structure."""
        self.data3 = {"nb_drones": None,
                      "start_hub": None,
                      "end_hub": None,
                      "hub": [],
                      "connection": []}

    def load_map(self, file: str) -> dict | None:
        """Load and parse the map file and return structured data."""
        try:
            with open(file, 'r') as f:
                data = f.read()

                for line in data.splitlines():
                    if line.startswith("#") or line == "":
                        continue
                    elif line.startswith("nb_drones: "):
                        self.data3["nb_drones"] = int(line.removeprefix(
                            "nb_drones: "))
                    elif line.startswith("start_hub: "):
                        temp = line.removeprefix("start_hub: ").split()
                        start = (temp[0], int(temp[1]), int(temp[2]), temp[3])
                        self.data3["start_hub"] = start
                    elif line.startswith("end_hub: "):
                        temp = line.removeprefix("end_hub: ").split()
                        self.data3["end_hub"] = (temp[0], int(temp[1]),
                                                 int(temp[2]), temp[3])
                    elif line.startswith("hub: "):
                        temp = line.removeprefix("hub: ").split()
                        self.data3["hub"].append((temp[0], int(temp[1]),
                                                 int(temp[2]), temp[3]))
                    elif line.startswith("connection: "):
                        self.data3["connection"].append(line.removeprefix(
                            "connection: "))
                if self.verif_data(self.data3) is True:
                    return self.data3
                else:
                    return None
        except FileNotFoundError:
            print("file not found for valid file use map/dict/file")

    def bold_red(self, text: str) -> str:
        """A function making strings of text bold red."""
        color, reset = "\033[1;91m", "\033[0m"
        return f"{color}{text}{reset}"

    def verif_data(self, data: dict) -> bool:
        try:

            if data["nb_drones"] < 0:
                raise Exception("error: number of drone is negatif value")
            start, x, y, color = data["start_hub"]
            if (isinstance(start, str) is False or x < 0 or y < 0
                    or "[color=" not in color):
                raise Exception("error: name of starthub or color is not str "
                                "or x or y is not number")
            end, x, y, color = data["end_hub"]
            if (isinstance(end, str) is False or x < 0 or y < 0
                    or "[color=" not in color):
                raise Exception("error: name of starthub or color is not str "
                                "or x or y is not number")
            if data["hub"]:
                for temp in data["hub"]:
                    hub, x, y, info = temp
                    if (isinstance(hub, str) is False or x < 0 or y < 0 or
                            "color=" not in info):
                        raise Exception("error: number of drone is negatif")
            if data["connection"]:
                for temp in data["connection"]:
                    if isinstance(temp, str) is False:
                        raise Exception("error: number of drone is negatif")
            return True
        except Exception as e:
            print(self.bold_red(e))
            return False


m = Parse()
print(m.load_map("maps/easy/01_linear_path.txt"))
