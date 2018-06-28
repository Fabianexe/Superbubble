"""The functions to handle the main function"""
from argparse import ArgumentParser
from LSD.inout import load
from LSD.partition import get_strongly_connected_component, create_auxiliary_graph
from LSD.dag_creation import construct_dag, choose_root, choose_random_root, construct_sung_graph
from LSD.detecter import dag_superbubble
from LSD.reporter import PrintReporter, PrintShortReporter, CountReporter, CompleteReporter, NullReporter
from LSD.filter import SungFilter, WeekFilter
from LSD.topological_sorting import toposort
import logging


__version__ = "1.0"
"""The version of the package"""

logger = None


def main():
    """The main function that does the superbubble detection.
    
    The detection is done with this code::
    
        dag, scc = partition.get_strongly_connected_component(g)
        for c in scc:
            partition.create_auxiliary_graph(c, g)
            if not (c.source_connected() or c.sink_connected()):
                dag_creation.choose_random_root(c)
                # includes tree construction
                dag_creation.construct_sung_graph(c)
                order = topological_sorting.toposort(c)
                # Use ComplexFilter for the sung superbubble filtering after detection
                detecter.dag_superbubble(c, order, filter.SungFilter(rep, order))
            else:
                dag_creation.choose_root(c)
                # includes tree construction
                dag_creation.construct_dag(c)
                order = topological_sorting.toposort(c)
                detecter.dag_superbubble(c, order, rep)
        partition.create_auxiliary_graph(dag, g)
        order = topological_sorting.toposort(dag)
        detecter.dag_superbubble(dag, order, rep)
    
    """
    global logger
    parser = ArgumentParser(prog='lsd', description="A simple tool to detect superbubbles.")

    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-v', '--verbose', action='store_true', dest="verbose", help="Create verbose output")
    parser.add_argument('path', action='store', help="The path to the input file")

    parser.add_argument('-f', '--format', action='store', dest="format", help="The format of the input file",
                        default="edgelist", choices=["edgelist", "adjlist", "gexf", "gml", "gpickle", "graph6",
                                                     "graphml", "leda", "pajek", "sparse6", "yaml"])
    parser.add_argument('--week', action='store_true', dest="week", help="Detect week superbubbles.")

    repo = parser.add_argument_group("Reporter", "The output reporter.")
    repo.add_argument('-r', '--reporter', action='store',  dest="reporter",
                            help="The reporter that is used to report the superbubbles",
                            default="print", choices=['print', 'sprint', 'count', 'complete', 'null'])
    repo.add_argument("-o", "--outpath", action='store', dest="outpath",
                      help="The path to the output file. Is used by complete reporter.", default="complete.out")
    
    args = parser.parse_args()

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
    logger.debug("Logging startet")
    
    # Load graph
    logger.debug("Load file in {format} from path: {path}.".format(format=args.format, path=args.path))
    g = load(args.path, args.format)
    logger.debug("Graph loaded")
    
    # Report type stuff 1
    rep = None
    
    if args.reporter == "print":
        logger.debug("Use simple print reporter.")
        rep = PrintReporter()
    elif args.reporter == "sprint":
        logger.debug("Use short print reporter.")
        rep = PrintShortReporter()
    elif args.reporter == "count":
        logger.debug("Use count reporter.")
        rep = CountReporter()
    elif args.reporter == "complete":
        logger.debug("Use complete reportor to {path}.".format(path=args.outpath))
        rep = CompleteReporter(g, args.outpath)
    elif args.reporter == "null":
        logger.debug("Use null reporter.")
        rep = NullReporter()

    # Only superbubbles and not week superbubbles
    if not args.week:
        rep = WeekFilter(rep, g)
        
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
            dag_superbubble(c, order, SungFilter(rep, order))
        else:
            logger.debug("Use gaertner algorithm")
            logger.debug("Choose root")
            choose_root(c)
            logger.debug("Construct DAG")
            # includes tree construction
            construct_dag(c)
            logger.debug("Construct topological ordering")
            order = toposort(c)
            logger.debug("Detect superbubbles")
            dag_superbubble(c, order, rep)
    logger.debug("Create auxiliary graph for DAG")
    create_auxiliary_graph(dag, g)
    logger.debug("Construct topological ordering")
    order = toposort(dag)
    logger.debug("Detect superbubbles")
    dag_superbubble(dag, order, rep)

    # Report type stuff 2
    logger.debug("Finalize output.")
    rep.fin()
    logger.debug("Finished.")
