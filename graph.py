import json

class GraphNode:
    def __init__(self, spread=False, n=None):
        self.s = spread
        self.n = n
        self.l = []
        self.activated = False

    def as_dict(self):
        return {
            "__class__" : "GraphNode",
            "spread" : self.s,
            "n" : self.n,
            "l" : self.l,
            "activated" : self.activated
        }

class Graph:
    def __init__(self):
        self.max = 0
        self.free = set()
        self.activated = set()
        self.nodes = {}

    def add_entry(self, node):
        if len(self.free) is 0:
            self.max += 1
            node.n = self.max
        else:
            node.n = self.free.pop()
        self.nodes[node.n] = node
        return node.n

    def remove_entry(self, n):
        node = self.nodes.pop(n)
        if n is self.max:
            self.max -= 1
        else:
            self.free.add(n)
        return node

    def spread(self):
        new = set()
        for o in self.activated:
            if not o.s:
                continue
            else:
                for v in o.l:
                    if not v.activated:
                        v.activated = True
                        new.add(v)
        self.activated = new.union(self.activated)

    def as_dict(self):
        return {
            "__class__" : "Graph",
            "max" : self.max,
            "free" : list(self.free),
            "activated" : list(self.activated),
            "nodes" : {n:self.nodes[n].as_dict() for n in self.nodes}
        }

    def as_json(self):
        return json.dumps(self.as_dict(), indent=2)

    def is_connex(self):
        goal = len(self.nodes)
        if goal is 0:
            return True
        active = {list(self.nodes.keys())[0]}
        found = {}
        while len(found) < goal and len(active) > 0:
            found += len(active)
            new = set()
            for v in active:
                for c in v.l:
                    if c not in found:
                        new.add(c)
            active = new

        return len(found) is goal

