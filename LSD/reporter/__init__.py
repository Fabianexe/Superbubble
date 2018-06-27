
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
    def __init__(self, g, path):
        self.t = time.time()
        self.head = "Vertices: {v}\nEdges: {e}\n".format(v=g.number_of_nodes(), e=g.number_of_edges())
        self.body = ""
        self.sum = 0
        self.path = path
    
    def rep(self, dag):
        self.body += "<{ind},{out}>\n".format(ind=dag[0], out=dag[-1])
        self.sum += 1
    
    def fin(self):
        self.head += "Elapsed time for processing: {t} secs.\nNumber of superbubbles found: {sum}.\n"\
            .format(t=time.time()-self.t, sum=self.sum)
        
        f = open(self.path, "w")
        f.write(self.head)
        f.write(self.body)

    
class NullReporter(Reporter):
    def rep(self, dag):
        pass
    
    def fin(self):
        pass
