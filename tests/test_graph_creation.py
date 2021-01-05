import pathlib

import pytest
from forcy import Forcy

from spacy.tokens import Doc
from spacy.vocab import Vocab

documents = [Doc(Vocab()).from_disk(p) for p in pathlib.Path("tests/docs").glob("*")]


@pytest.mark.parametrize("doc", documents)
def test_graph_size(doc):
    fdoc = Forcy(doc)
    assert len(fdoc.graph.nodes) == len(doc)
    assert len(fdoc.graph.edges) == (len(doc) - 1)


@pytest.mark.parametrize("prog", ["dot", "twopi", "fdp", "sfdp"])
@pytest.mark.parametrize("doc", documents)
def test_graph_size(doc, prog):
    fdoc = Forcy(doc)
    nodes = fdoc._d3_coordinates(prog=prog)["nodes"]
    links = fdoc._d3_coordinates(prog=prog)["links"]
    assert len(nodes) == len(doc)
    assert len(links) == (len(doc) - 1)
