"""
This module provides a class to represent circuits as graphs.
This is primarily for loop analysis but is also used for nodal analysis.

Copyright 2019--2022 Michael Hayes, UCECE

"""

import networkx as nx


# V1 1 0 {u(t)}; down
# R1 1 2; right=2
# L1 2 3; down=2
# W1 0 3; right
# W 1 5; up
# W 2 6; up
# C1 5 6; right=2

def canonical_loop(cycle):
    """Rearrange node order for loop into canonical form."""

    def rotate(l, n):
        return l[n:] + l[:n]

    # Preserve node order.
    sorted_cycle = sorted(cycle)
    index = cycle.index(sorted_cycle[0])
    new_cycle = rotate(cycle, index)
    if new_cycle[1] > new_cycle[-1]:
        # Reverse ordering.
        new_cycle = new_cycle[0:1] + new_cycle[:0:-1]
    return new_cycle


class CircuitGraph(object):

    @classmethod
    def from_circuit(cls, cct):

        G = nx.Graph()

        dummy = 0
        # Dummy nodes are used to avoid parallel edges.
        dummy_nodes = {}

        G.add_nodes_from(cct.node_list)

        node_map = cct.node_map

        for name in cct.branch_list:
            elt = cct.elements[name]
            if len(elt.node_names) < 2:
                continue

            node_name1 = node_map[elt.node_names[0]]
            node_name2 = node_map[elt.node_names[1]]

            if G.has_edge(node_name1, node_name2):
                # Add dummy node in graph to avoid parallel edges.
                dummynode = '*%d' % dummy
                dummycpt = 'W%d' % dummy
                G.add_edge(node_name1, dummynode, name=name)
                G.add_edge(dummynode, node_name2, name=dummycpt)
                dummy_nodes[dummynode] = node_name2
                dummy += 1
            else:
                G.add_edge(node_name1, node_name2, name=name)

        return cls(cct, G)

    def __init__(self, cct, G=None):

        # For backwards compatibility
        if G is None:
            G = self.from_circuit(cct).G

        self.cct = cct
        self.node_map = cct.node_map
        self.G = G

    def connected_cpts(self, node):
        """Components connected to specified node."""

        for node1, edges in self.node_edges(node).items():
            if node1.startswith('*'):
                for elt in self.connected_cpts(node1):
                    yield elt
                continue

            for key, edge in edges.items():
                if not edge.startswith('W'):
                    elt = self.cct.elements[edge]
                    yield elt

    def connected(self, node):
        """Set of component names connected to specified node."""

        return set([cpt.name for cpt in self.connected_cpts(node)])

    def all_loops(self):

        # This adds forward and backward edges.
        DG = nx.DiGraph(self.G)
        cycles = list(nx.simple_cycles(DG))

        loops = []
        for cycle in cycles:
            if len(cycle) <= 2:
                continue
            cycle = canonical_loop(cycle)
            if cycle not in loops:
                loops.append(cycle)
        return loops

    def chordless_loops(self):

        loops = self.all_loops()
        sets = [set(loop) for loop in loops]

        DG = nx.DiGraph(self.G)

        rejects = []
        for i in range(len(sets)):

            # Reject loops with chords.
            loop = loops[i]
            if len(loop) == 2:
                continue

            for j in range(i + 1, len(sets)):
                if sets[i].issubset(sets[j]):
                    rejects.append(j)
                elif sets[j].issubset(sets[i]):
                    rejects.append(i)

        cloops = []
        for i, loop in enumerate(loops):
            if i not in rejects:
                cloops.append(loop)

        return cloops

    def cut_sets(self):
        """Return list of cut sets.  Each cut set is a set of nodes describing
        a sub-graph G'.  Removing all the edges of G' from the graph
        disconnects it.  This will fail if there are unconnected
        components."""

        # It may be better to return a list of sets of edges.

        if hasattr(self, '_cutsets'):
            return self._cutsets
        self._cutsets = list(nx.all_node_cuts(self.G))
        return self._cutsets

    def cut_vertices(self):
        """Return list of cut vertices.  Each cut vertex is a node
        that if removed, with its edges, disconnects the graph."""

        return list(nx.articulation_points(self.G))

    def cut_edges(self):
        """Return list of cut edges.  Each cut edge is an edge that
        disconnects the graph if removed."""

        return list(nx.minimum_edge_cut(self.G))

    def loops(self):
        """Return list of loops:  Each loop is a list of nodes."""

        if hasattr(self, '_loops'):
            return self._loops
        self._loops = self.chordless_loops()
        return self._loops

    def loops_by_cpt_name(self):
        """Return list of loops specified by cpt name."""

        ret = []
        for loop in self.loops():
            foo = []
            for m in range(len(loop) - 1):
                cpt = self.component(loop[m + 1], loop[m])
                if cpt is None:
                    continue

                foo.append(cpt.name)
            foo.append(self.component(loop[-1], loop[0]).name)
            ret.append(foo)
        return ret

    def draw(self, filename=None):
        """Use matplotlib to draw circuit graph."""

        from matplotlib.pyplot import subplots, savefig

        fig, ax = subplots(1)

        G = self.G
        pos = nx.spring_layout(G)

        labels = dict(zip(G.nodes(), G.nodes()))
        nx.draw_networkx(G, pos, ax, labels=labels)

        edge_labels = dict([((u, v), d['name'])
                            for u, v, d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        if filename is not None:
            savefig(filename, bbox_inches='tight')

    @property
    def is_planar(self):
        """Return True for a planar network."""

        return nx.check_planarity(self.G)[0]

    @property
    def nodes(self):
        """Return nodes comprising network."""

        return self.G.nodes()

    def node_edges(self, node):
        """Return edges connected to specified node."""

        return self.G[node]

    def component(self, node1, node2):
        """Return component connected between specified nodes."""

        name = self.G.get_edge_data(node1, node2)['name']
        if name.startswith('W'):
            return None
        return self.cct.elements[name]

    def loops_for_cpt(self, elt):
        """Return list of tuples; one for each loop.  The first element of the
        tuple is the loop the cpt belongs to or an empty list; the
        second element indicates the cpt direction compared to the
        loop direction."""

        loops = self.loops()
        cloops = []

        # Map node names to equipotential node names.
        node_names = [self.cct.node_map[node_name] for node_name in elt.node_names]

        for n, loop in enumerate(loops):

            loop1 = loop.copy()
            loop1.append(loop1[0])

            def find(loop1, node_name1, node_name2):
                for m in range(len(loop1) - 1):
                    if (node_name1 == loop1[m] and
                            node_name2 == loop1[m + 1]):
                        return True

            if find(loop1, node_names[0], node_names[1]):
                cloops.append((loop, False))
            elif find(loop1, node_names[1], node_names[0]):
                cloops.append((loop, True))
            else:
                cloops.append(([], None))

        return cloops

    @property
    def components(self):
        """Return list of component names."""

        return [d['name'] for n1, n2, d in self.G.edges(data=True)]

    def in_series(self, cpt_name):
        """Return set of component names in series with cpt including itself."""

        # FIXME: determine R1 in series for R3 for R1 + (R2 | L) + R3
        # FIXME: R1 and R2 not in series for R1 | R2

        cct = self.cct
        elt = cct.elements[cpt_name]
        node_names = [cct.node_map[node_name] for node_name in elt.node_names]

        series = []
        series.append(cpt_name)

        def follow(node):
            neighbours = self.G[node]
            if len(neighbours) > 2:
                return
            for n, e in neighbours.items():
                if not e['name'] in series:
                    series.append(e['name'])
                    follow(n)

        follow(node_names[0])
        follow(node_names[1])

        # If only have two components in parallel, they will be
        # detected as a series connection.  However, if there is a
        # dummy wire, the components are in parallel.
        for name in series:
            if name.startswith('W'):
                return set((cpt_name, ))

        return set(series)

    def in_parallel(self, cpt_name):
        """Return set of component names in parallel with cpt including itself."""

        cct = self.cct
        elt = cct.elements[cpt_name]
        node_names = [cct.node_map[node_name] for node_name in elt.node_names]

        n1, n2 = node_names[0:2]

        # This is trivial for a multigraph but a mutigraph adds
        # additional problems since component() will fail if have
        # multiple edges between the same nodes.
        # edges = self.get_edge_data(n1, n2)
        # parallel = [d['name'] for k, d in edges.items()]

        parallel = [cpt_name]

        neighbours1 = self.G[n1]
        neighbours2 = self.G[n2]

        # The first created parallel component has no dummy nodes.
        try:
            name = self.G.get_edge_data(n1, n2)['name']
            parallel.append(name)
        except:
            pass

        # If find a dummy node name then there is a parallel component.

        for n, e in neighbours1.items():
            if n.startswith('*'):
                for n3, e3 in self.G[n].items():
                    if n3 == n2 and not e['name'].startswith('W'):
                        parallel.append(e['name'])
        for n, e in neighbours2.items():
            if n.startswith('*'):
                for n3, e3 in self.G[n].items():
                    if n3 == n1 and not e['name'].startswith('W'):
                        parallel.append(e['name'])

        if n1.startswith('*'):
            for n3, e3 in self.G[n1].items():
                if n3 == n2 and not e['name'].startswith('W'):
                    parallel.append(e['name'])
        if n2.startswith('*'):
            for n3, e3 in self.G[n2].items():
                if n3 == n1 and not e['name'].startswith('W'):
                    parallel.append(e['name'])

        return set(parallel)

    @property
    def node_connectivity(self):
        """Return node connectivity for graph.  If the connectivity is 0,
        then there are disconnected components.  If there is a component
        with a single connected node, the connectivity is 1."""

        return nx.node_connectivity(self.G)

    @property
    def is_connected(self):
        """Return True if all components are connected."""

        return self.node_connectivity != 0

    def tree(self):
        """Return minimum spanning tree.  A tree has no loops so no current flows."""

        T = nx.minimum_spanning_tree(self.G)
        return CircuitGraph(self.cct, T)

    def links(self):
        """Return links; the graph of the edges that are not in the minimum
        spanning tree."""
        G = self.G
        T = self.tree().G

        G_edges = set(G.edges())
        T_edges = set(T.edges())

        L_edges = G_edges - T_edges

        L = nx.Graph()
        for edge in L_edges:
            data = G.get_edge_data(*edge)
            L.add_edge(*edge, name=data['name'])
        return CircuitGraph(self.cct, L)

    @property
    def num_parts(self):

        if self.is_connected:
            return 1
        raise ValueError('TODO, calculate number of separate graphs')

    @property
    def num_nodes(self):
        """The number of nodes in the graph."""

        return len(self.G.nodes)

    @property
    def num_branches(self):
        """The number of branches (edges) in the graph."""

        return len(self.G.edges)

    @property
    def rank(self):
        """The required number of node voltages for nodal analysis."""

        return self.num_nodes - self.num_parts

    @property
    def nullity(self):
        """For a planar circuit, this is equal to the number of meshes in the graph."""

        return self.num_branches - self.num_nodes + self.num_parts

    def pdb(self):

        import pdb
        pdb.set_trace()
        return self
