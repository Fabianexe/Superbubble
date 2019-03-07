"""The functions to handle the main function"""
from argparse import ArgumentParser
from LSD.inout import load
from LSD.detecter.onodera import onodera

import logging

from LSD.detecter.gaertner import dag_superbubble
from LSD.detecter.brankovic import super_bubble_brankovice
from LSD.dag_creation.sung import construct_sung_graph
from LSD.dag_creation import construct_dag
from LSD.dag_creation.roots import choose_random_root, choose_root
from LSD.filter import MiniFilter, InnerFilter, SortFilter, SungFilter, WeekFilter, SCCFilter
from LSD.reporter import PrintReporter, PrintShortReporter, CountReporter, CompleteReporter, NullReporter
from LSD.partition import get_strongly_connected_component
from LSD.auxiliary_graph import create_auxiliary_graph
from LSD.topological_sorting import toposort
from LSD.colorgraph import ColorGraph
from LSD.roots import generate_roots
from LSD.dfs_tree.order import create_dfs_order, create_dfs_order_cycle
from LSD.detecter import superbubble

__version__ = "2.0"
"""The version of the package"""

logger = None


def main():
    """The main function that loads the commands."""
    global logger

    parent = ArgumentParser(prog='lsd', description="A simple tool to detect superbubbles.", add_help=False)

    parent.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parent.add_argument('-v', '--verbose', action='store_true', dest="verbose", help="Create verbose output")
    parent.add_argument('path', action='store', help="The path to the input file. Use '-' for stdin.")

    parent.add_argument('-f', '--format', action='store', dest="format", help="The format of the input file",
                        default="edgelist", choices=["edgelist", "adjlist", "gexf", "gml", "gpickle", "graph6",
                                                     "graphml", "leda", "pajek", "sparse6", "yaml"])

    filt = parent.add_argument_group("Filter", "The output filter. More then one can be applied.")

    filt.add_argument('--week', action='store_true', dest="week", help="Detect week superbubbles.")
    filt.add_argument('--sort', action='store_true', dest="sort", help="Sort output by source id.")
    filt.add_argument('--mini', action='store_true', dest="mini", help="Remove superbubble+üö  of size 2.")
    filt.add_argument('--inner', action='store_true', dest="inner", help="Only report not included superbubbles.")

    repo = parent.add_argument_group("Reporter", "The output reporter. Only one can be applied. " +
                                     "When nothing is given the print reporter is used.")
    repo.add_argument('--print', action='store_true', dest="print", help="Print on stdout the complete superbubble.")
    repo.add_argument('--sprint', action='store_true', dest="sprint",
                      help="Print on stdout the s and t of a superbubble.")
    repo.add_argument('--count', action='store_true', dest="count", help="Print on stdout the number of superbubbles.")
    repo.add_argument('--null', action='store_true', dest="null", help="Report nothing.")
    repo.add_argument('--complete', action='store', dest="outpath",
                      help="Give a path where a complete output is written. Use '-' for stdout.")
    
    parser = ArgumentParser(prog='lsd', description="A simple tool to detect superbubbles.")

    parser.set_defaults(comand=False)
    
    subparsers = parser.add_subparsers(title='Methods')
    det = subparsers.add_parser('detect', help="Detect superbubbles.", aliases=['d'], parents=[parent])
    det.set_defaults(func=detection, comand=True)
    ono = subparsers.add_parser('onodera', help="Use the onodera algorithm.", aliases=['o'], parents=[parent])
    ono.set_defaults(func=onodera_detection, comand=True)
    part = subparsers.add_parser('part', help="Use the portioning approach.", aliases=['p'], parents=[parent])
    part.set_defaults(func=part_detection, comand=True)

    part.add_argument('--sung', action='store_true', dest="sung", help="Use sung graph instead.")
    part.add_argument('--brankovic', action='store_true', dest="brankovic", help="Uses brankovic detector")
    
    args = parser.parse_args()
    
    if not args.comand:
        parser.print_help()
        exit(0)
    
    # Logger stuff
    if logger is None:
        level = logging.INFO
        if args.verbose:
            level = logging.DEBUG
        logger = logging.Logger(name="logging loui")
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter("%(levelname)-5s %(asctime)s: %(message)s", "%H:%M:%S")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    logger.debug("Start lsd version {v}".format(v=__version__))
    
    if len([x for x in ("print", "sprint", "null", "count", "outpath") if vars(args)[x]]) > 1:
        print("Give only one reporter!")
        exit(1)
    
    # Load graph
    logger.debug("Load file in {format} from path: {path}.".format(format=args.format, path=args.path))
    g = load(args.path, args.format)
    logger.debug("Graph loaded")
    
    # Report type stuff 1
    if args.sprint:
        logger.debug("Use short print reporter.")
        rep = PrintShortReporter()
    elif args.count:
        logger.debug("Use count reporter.")
        rep = CountReporter()
    elif args.outpath:
        logger.debug("Use complete reporter to {path}.".format(path=args.outpath))
        rep = CompleteReporter(g, args.outpath)
    elif args.null:
        logger.debug("Use null reporter.")
        rep = NullReporter()
    else:
        logger.debug("Use simple print reporter.")
        rep = PrintReporter()
    
    # Filter stuff
    if args.sort:
        logger.debug("Sort filter is applied.")
        rep = SortFilter(rep)
    if args.mini:
        logger.debug("Mini filter is applied.")
        rep = MiniFilter(rep)
    if args.inner:
        logger.debug("Inner filter is applied.")
        rep = InnerFilter(rep)
    if not args.week:
        logger.debug("Week superbublle filter is applied.")
        rep = WeekFilter(rep, g)

    args.func(g, rep, args)
    
    # Report type stuff 2
    logger.debug("Finalize output.")
    rep.fin()
    logger.debug("Finished.")


def onodera_detection(g, rep, *_):
    logger.debug("Start onodera algorithm.")
    onodera(g, rep)


def detection(graph, rep, *_):
    logger.debug("Start gaertner 2019 algorithm.")
    g = ColorGraph(graph)
    for v, cycle in generate_roots(g):
        if cycle:
            order, v2 = create_dfs_order_cycle(v, g)
            superbubble(g, order, SCCFilter(rep, v, v2), v, v2)
        else:
            order = create_dfs_order(v, g)
            superbubble(g, order, rep, v)


def part_detection(g, rep, args):
    logger.debug("Start part algorithm.")
    # Use brankovic
    if args.brankovic:
        logger.debug("Use brankovic algorithm.")
        detect = super_bubble_brankovice
    else:
        logger.debug("Use gaertner 2018 algorithm to detect.")
        detect = dag_superbubble
    
    # Use sung
    if args.sung:
        logger.debug("Use sung algorithm.")
        construct = construct_sung_graph
        
        def detect2(c2, order2, rep2):
            return detect(c2, order2, SungFilter(rep2, order2, c2))
    else:
        logger.debug("Use gaertner 2018 algorithm to part construction.")
        construct = construct_dag
        detect2 = detect
    
    # Detect superbubble
    logger.debug("Find SCCs.")
    dag, scc = get_strongly_connected_component(g)
    logger.debug("Iterate over SCCs.")
    for c in scc:
        logger.debug("Start with  SCCs " + str(c.nr))
        logger.debug("Create auxiliary graph")
        create_auxiliary_graph(c, g)
        if not (c.source_connected() or c.sink_connected()):
            logger.debug("Use sung algorithm")
            logger.debug("Choose root")
            choose_random_root(c)
            logger.debug("Construct DAG")
            # includes tree construction
            construct_sung_graph(c)
            logger.debug("Construct topological ordering")
            order = toposort(c)
            logger.debug("Detect superbubbles")
            # Use ComplexFilter for the sung superbubble filtering after detection
            detect(c, order, SungFilter(rep, order))
        else:
            logger.debug("Use gaertner algorithm")
            logger.debug("Choose root")
            choose_root(c)
            logger.debug("Construct DAG")
            # includes tree construction
            construct(c)
            logger.debug("Construct topological ordering")
            order = toposort(c)
            logger.debug("Detect superbubbles")
            detect2(c, order, rep)
    logger.debug("Create auxiliary graph for DAG")
    create_auxiliary_graph(dag, g)
    logger.debug("Construct topological ordering")
    order = toposort(dag)
    logger.debug("Detect superbubbles")
    detect(dag, order, rep)
