import sys
from load_map import Parse
from Graph import Graph

try:
    if 1 < len(sys.argv):
        parse = Parse()

        data = parse.load_map(sys.argv[1])
        if data is None:
            raise Exception("data is None data is invalid in map")
        graph = Graph(data)
        graph.run()
    else:
        print("Usage: python3 Fly_in.py <map_file>")
except Exception as e:
    print(f"Erreur lors de la simulation : {e}")
