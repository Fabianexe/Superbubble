from argparse import ArgumentParser
from LSD.inout import load
import LSD.tools as t

if __name__ == "__main__":
    parser = ArgumentParser(prog='tool', description="A simple tool to check superbubbles.")
    parser.add_argument('path', action='store', help="The path to the input file")
    parser.add_argument('-f', '--format', action='store', dest="format", help="The format of the input file",
                        default="edgelist", choices=["edgelist", "adjlist", "gexf", "gml", "gpickle", "graph6",
                                                     "graphml", "leda", "pajek", "sparse6", "yaml"])
    parser.add_argument('-s', '--superbubble', action='append', dest="sup",
                        help="The printed superbubbles")
    args = parser.parse_args()

    print("Load file")
    g = load(args.path, args.format)
    print("File loaded")
    for s in args.sup:
        print("Start with superbubble " + s)
        i, j = s.split(",")
        t.draw_graph(t.get_superbubble(i, j, g),"{i}_{j}.png".format(i=i, j=j))
    print("Finished.")