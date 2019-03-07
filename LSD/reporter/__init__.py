
from abc import ABC, abstractmethod
import time


class Reporter(ABC):
    @abstractmethod
    def rep(self, dag):
        pass

    @abstractmethod
    def fin(self):
        pass


class PrintReporter(Reporter):
    def rep(self, dag):
        print(dag)
    
    def fin(self):
        pass


class PrintShortReporter(Reporter):
    def rep(self, dag):
        print("<{ind},{out}>".format(ind=dag[0], out=dag[-1]))
    
    def fin(self):
        pass


class CountReporter(Reporter):
    def __init__(self):
        self.sum = 0
    
    def rep(self, dag):
        self.sum += 1
    
    def fin(self):
        print("Number of superbubbles found: {sum}.".format(sum=self.sum))


class CompleteReporter(Reporter):
    """Write a file with informations about the graph the detection time,
    the number of superbubbles and a list of superbubbles.
    Inspired by the output of SUPBUB.
    The superbubble <1,4> creates the output:
    <1,4>"""
    
    def __init__(self, g, path):
        self.head = "Vertices: {v}\nEdges: {e}\n".format(v=g.number_of_nodes(), e=g.number_of_edges())
        self.body = []
        self.sum = 0
        self.path = path
        self.t = time.time()
    
    def rep(self, dag):
        self.body.append((dag[0], dag[-1]))
        self.sum += 1
    
    def fin(self):
        self.head += "Elapsed time for processing: {t} secs.\nNumber of superbubbles found: {sum}.\n" \
            .format(t=time.time() - self.t, sum=self.sum)
        self.body.sort()
        if self.path == "-":
            from sys import stdout
            f = stdout
        else:
            f = open(self.path, "w")
        f.write(self.head)
        for dag in self.body:
            f.write("<{ind},{out}>\n".format(ind=dag[0], out=dag[-1]))
    
class NullReporter(Reporter):
    """Report nothing at all. Can be used for time test."""
    def rep(self, dag):
        pass
    
    def fin(self):
        pass
