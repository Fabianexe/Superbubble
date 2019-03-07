from LSD.reporter import Reporter


class Filter(Reporter):
    def __init__(self, reporter):
        self.reporter = reporter
        
    def report(self, dag):
        self.reporter.rep(dag)
        
    def fin(self):
        self.reporter.fin()
    
    def rep(self, dag):
        pass


class ComplexFilter(Filter):
    def __init__(self, reporter, order):
        super().__init__(reporter)
        self.dags = set()
        self.order = order
    
    def rep(self, dag):
        source = str(dag[0])
        sink = str(dag[-1])
        if sink.endswith("_2"):
            if source.endswith("_2"):
                self.dags.add((source[:-2], sink[:-2]))
            elif self.order.get_position(sink[:-2]) < self.order.get_position(source):
                for i in range(len(dag)):
                    if dag[i].endswith("_2"):
                        dag[i] = dag[i][:-2]
                self.report(dag)
        else:
            if (source, sink) in self.dags:
                self.report(dag)
                

class MiniFilter(Filter):
    def __init__(self, reporter):
        super().__init__(reporter)
    
    def rep(self, dag):
        if len(dag) > 2:
            self.report(dag)


class InnerFilter(Filter):
    def __init__(self, reporter):
        super().__init__(reporter)
        self.dags = []
    
    def rep(self, dag):
        self.dags.insert(0, dag)
    
    def fin(self):
        inner = set()
        for d in self.dags:
            if d[0] not in inner:
                self.report(d)
            if len(d) > 2:
                inner.update(d[1:-1])
        super().fin()


class SortFilter(Filter):
    def __init__(self, reporter):
        super().__init__(reporter)
        self.dags = []
    
    def rep(self, dag):
        self.dags.append(dag)
    
    def fin(self):
        self.dags.sort(key=lambda x: (int(x[0]), int(x[-1])))
        for d in self.dags:
            self.report(d)
        super().fin()


class SungFilter(Filter):
    """The sung filter to get only the right superbubbles."""
    
    def __init__(self, reporter, order, c=None):
        super().__init__(reporter)
        self.dags = set()
        self.order = order
        self.c = c
    
    def rep(self, dag):
        source = str(dag[0])
        sink = str(dag[-1])
        if sink.endswith("_2"):
            if source.endswith("_2"):
                self.dags.add((source[:-2], sink[:-2]))
            elif self.order.index(sink[:-2]) < self.order.index(source):
                for i in range(len(dag)):
                    if dag[i].endswith("_2"):
                        dag[i] = dag[i][:-2]
                if self.c is not None:
                    for i in range(0, len(dag) - 1):
                        if self.c.b in self.c.successors(dag[i] + "_2"):
                            return
                    for i in range(1, len(dag)):
                        if self.c.a in self.c.predecessors(dag[i]):
                            return
                self.report(dag)
        else:
            if (source, sink) in self.dags:
                self.report(dag)


class WeekFilter(Filter):
    """The filter that to get only superbubbles and discards week superbubbles."""
    
    def __init__(self, reporter, g):
        super().__init__(reporter)
        self.g = g
    
    def rep(self, dag):
        if not dag[0] in self.g.successors(dag[-1]):
            self.report(dag)


class SCCFilter(Filter):
    """The filter that correct the artificial vertex and discards false added superbubble."""
    
    def __init__(self, reporter, v, v2):
        super().__init__(reporter)
        self.v = v
        self.v2 = v2
    
    def rep(self, dag, ):
        if dag[-1] == self.v2:
            dag[-1] = self.v
        if dag[0] != dag[-1]:
            self.report(dag)