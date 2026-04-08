class Parse():
    """Parse a drone map config file."""
    def __init__(self) -> None:
        """Initialize the parser with an empty data structure."""
        self.data3 = {"nb_drones": None,
                      "start_hub": None,
                      "end_hub": None,
                      "hub": [],
                      "connection": []}

    def __Parsemetadata(self, parts: list[str]) -> dict:
        """Extract tags like color=#FF0000 or max_drones=5
        from a list of strings."""
        meta = {"zone": "normal", "color": "none", "max_drones": 1}
        for i in parts:
            if "=" in i:
                i = i.strip("[]")
                key, f = i.split("=", 1)
                if key == "zone" and f not in ["normal", "blocked",
                                               "restricted", "priority"]:
                    raise Exception(f"Invalid zone type: {f}")
                if key == "max_drones":
                    f = int(f)
                meta[key] = f
        return meta

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
                        if self.data3["start_hub"] is not None:
                            raise Exception("stard_hub exicte deja")
                        temp = line.removeprefix("start_hub: ").split()
                        start = (temp[0], int(temp[1]), int(temp[2]),
                                 self.__Parsemetadata(temp[3:]))
                        self.data3["start_hub"] = start
                    elif line.startswith("end_hub: "):
                        if self.data3["end_hub"] is not None:
                            raise Exception("end_hub exicte deja")
                        temp = line.removeprefix("end_hub: ").split()
                        self.data3["end_hub"] = (temp[0], int(temp[1]),
                                                 int(temp[2]),
                                                 self.__Parsemetadata(temp[3:])
                                                 )
                    elif line.startswith("hub: "):
                        temp = line.removeprefix("hub: ").split()
                        self.data3["hub"].append((temp[0], int(temp[1]),
                                                 int(temp[2]),
                                                 self.__Parsemetadata(temp[3:])
                                                  ))
                    elif line.startswith("connection: "):
                        temp = line.removeprefix("connection: ").split()
                        if len(temp) > 1:
                            meta = self.__Parsemetadata(temp[1:])
                            self.data3["connection"].append((temp[0], meta))
                        else:
                            self.data3["connection"].append(temp[0].split("-"))

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
        """verif of data"""
        try:
            if data["nb_drones"] is None or data["nb_drones"] <= 0:
                raise Exception("error: number of drone is <= 0")
            if data["start_hub"] is not None:
                start, x, y, meta = data["start_hub"]
                if (isinstance(start, str) is False
                        or isinstance(y, int) is False
                        or isinstance(x, int) is False or meta is None
                        or "-" in start or " " in start):
                    raise Exception("error: name of starthub or color is not"
                                    " str or x or y is not number")
            else:
                raise Exception("no data for start hub")
            if data["end_hub"] is not None:
                end, x, y, meta = data["end_hub"]
                if (isinstance(end, str) is False
                        or isinstance(y, int) is False
                        or isinstance(x, int) is False or meta is None
                        or "-" in end or " " in end):
                    raise Exception("error: name of starthub or color is not"
                                    " str or x or y is not number")
            else:
                raise Exception("no data for end hub")
            if data["hub"]:
                for temp in data["hub"]:
                    hub, x, y, info = temp
                    if (isinstance(hub, str) is False
                            or isinstance(y, int) is False
                            or isinstance(x, int) is False or
                            info is None or "-" in hub or " " in hub):
                        raise Exception("error: number of drone is negatif")
            if data["connection"]:
                seen = set()
                for temp in data["connection"]:
                    hub_name = [item for item in temp if isinstance(item, str)]

                    if len(hub_name) < 2:
                        continue

                    for name in hub_name:
                        if (isinstance(name, str) is False or "-" in name
                                or " " in name):
                            raise Exception("error:")
                    key = tuple(sorted(hub_name))
                    if key in seen:
                        raise Exception(f"error: duplicate connection {temp}")
                    seen.add(key)
            return True
        except Exception as e:
            print(self.bold_red(str(e)))
            return False


m = Parse()
print(m.load_map("maps/hard/02_capacity_hell.txt"))
