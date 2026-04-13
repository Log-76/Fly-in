import sys
from load_map import Parse
from Graph import Graph


if 1 < len(sys.argv):
    parse = Parse()

    data = parse.load_map(sys.argv[1])
    graph = Graph(data)
    graph.run()
    print(graph.drones)
