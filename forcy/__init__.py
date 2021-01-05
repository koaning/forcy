from spacy.tokens import Doc
from forcy._forcy import Forcy


def _make_forcy_mpl(doc, prog='twopi'):
    return Forcy(doc).plot_mpl(prog=prog)


def _nxgraph(doc):
    return Forcy(doc).graph


def set_extensions():
    Doc.set_extension("plot_graph_mpl", method=_make_forcy_mpl)
    Doc.set_extension("nxgraph", method=_nxgraph)


__all__ = ['set_extensions', "Forcy"]
