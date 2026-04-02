def load_map(file: str) -> dict:
    try:
        with open(file, 'r') as f:
            data = f.read()
            data2 = data.splitlines()
            data3 = []
            for f in data2:
                if f.startswith("nb_drones: "):
                    data3.append(int(f.removeprefix("nb_drones: ")))
                if f.startswith("start_hub: "):
                    data3.append(f.removeprefix("start_hub: "))
                if f.startswith("end_hub: "):
                    data3.append(f.removeprefix("end_hub: "))
                if f.startswith("hub: "):
                    data3.append(f.removeprefix("hub: "))
                if f.startswith("connection: "):
                    data3.append(f.removeprefix("connection: "))

            print(data3)
    except FileNotFoundError:
        print("file not found for valid file use map/dict/file")


load_map("maps/easy/01_linear_path.txt")
