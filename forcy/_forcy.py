import json
import random
import pathlib
from string import Template

import networkx as nx
import matplotlib.pyplot as plt
from spacy.tokens import Token
from IPython.core.display import HTML
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.algorithms.simple_paths import all_simple_paths, all_simple_edge_paths


class Forcy:
    """
    Creates a Forcy object. It contains both the spaCy doc and some networkx helpers.
    """

    def __init__(self, doc):
        self.doc = doc
        self.graph = nx.DiGraph()
        self._populate_graph(doc)
        self.idx_translation = {t.text: i for i, t in enumerate(doc)}  # beware, not a 1-1 mapping
        self.text_translation = {i: t.text for i, t in enumerate(doc)}

    def _populate_graph(self, doc):
        """
        Takes the doc and adds it's relevant properties to the graph.
        """
        for idx, t in enumerate(self.doc):
            self.graph.add_node(idx, **self._grab_useful_tok_info(t))
        translation = {t.idx: i for i, t in enumerate(doc)}
        for tok in self.doc:
            for child in tok.children:
                self.graph.add_edge(translation[tok.idx], translation[child.idx], dep=child.dep_)

    @staticmethod
    def _grab_useful_tok_info(tok: Token):
        """
        Ensure we add useful information to the node.
        """
        return {"pos": tok.pos_, "text": tok.text, "lemma": tok.lemma_, "lower": tok.lower_, "like_num": tok.like_num}

    def _random_string(self):
        return "".join([random.choice("qwertyuiopasdfghjklzxcvbnm") for _ in range(4)])

    def pretty_plot_coordinates(self, prog="dot"):
        """
        Generated coordinates for pretty visualisation.

        Arguments:
            - prog: the layout program from graphviz, can be either `dot`,`twopi`,`fdp`,`sfdp`
        """
        return graphviz_layout(self.graph, prog=prog)

    def _d3_coordinates(self, prog="dot"):
        """
        Generated coordinates for pretty visualisation.

        Arguments:
            - prog: the layout program from graphviz, can be either `dot`,`twopi`,`fdp`,`sfdp`
        """
        node_data = []
        for k, v in self.pretty_plot_coordinates(prog=prog).items():
            d = {'coords': {"x": v[0], "y": v[1]}, 'idx': k, 'text': self.graph.nodes[k]['text'], 'pos': self.graph.nodes[k]['pos']}
            node_data.append(d)
        link_data = [{'source': node_data[s]['coords'], 'target': node_data[t]['coords'], **self.graph.edges[(s, t)]}
                     for s, t in self.graph.edges]
        return {"nodes": node_data, "links": link_data}

    def d3_plot(self, prog="dot"):
        """
        Generate a d3 plot for jupyterlab.

        Arguments:
            - prog: the layout program from graphviz, can be either `dot`,`twopi`,`fdp`,`sfdp`
        """
        t = Template(pathlib.Path("_index.html").read_text())
        rendered = t.substitute({'data': json.dumps(self._d3_coordinates(prog=prog)), 'tmpid': self._random_string()})
        return HTML(rendered)

    def plot_mpl(self, prog="dot"):
        """
        Use matplotlib to make a pretty graph plot.

        Arguments:
            - prog: the layout program from graphviz, can be either `dot`,`twopi`,`fdp`,`sfdp`
        """
        nx.draw(self.graph, self.pretty_plot_coordinates(prog=prog))
        plt.show()

    def text_appears_many_times(self, text):
        return len([t for t in self.doc if t.text == text]) > 1

    def path(self, start, end):
        """
        Prints the path from one word in the document to another.

        You can only supply words that appear only once in the document.
        """
        if self.text_appears_many_times(start):
            raise ValueError(f"Cannot use shorthand {start} because it appears multiple times in doc.")
        if self.text_appears_many_times(end):
            raise ValueError(f"Cannot use shorthand {end} because it appears multiple times in doc.")
        source, sink = self.idx_translation[start], self.idx_translation[end]
        node_names = [self.doc[n] for n in next(all_simple_paths(self.graph, source, sink))]
        edge_names = [self.graph.edges[(i, j)]['dep'] for i, j in next(all_simple_edge_paths(self.graph, source, sink))]
        fin_doc = node_names[-1]
        return "".join(f"{d}|{d.pos_} -[{e}]-> " for d, e in zip(node_names, edge_names)) + f"{fin_doc}|{fin_doc.pos_}"
