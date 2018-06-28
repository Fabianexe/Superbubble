from LSD.reporter import Reporter


class Filter(Reporter):
    """Abstract filter class that every Filter implements."""
    def __init__(self, reporter):
        self.reporter = reporter
        
    def report(self, dag):
        self.reporter.rep(dag)
        
    def fin(self):
        self.reporter.fin()
    
    def rep(self, dag):
        pass


class SungFilter(Filter):
    """The sung filter to get only the right superbubbles."""
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


class WeekFilter(Filter):
    """The filter that to get only superbubbles and discards week superbubbles."""
    def __init__(self, reporter, g):
        super().__init__(reporter)
        self.g = g

    def rep(self, dag):
        if not dag[0] in self.g.successors(dag[-1]):
            self.report(dag)
