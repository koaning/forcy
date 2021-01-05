import pathlib
import pytest
import forcy

from networkx import Graph

from spacy.tokens import Doc
from spacy.vocab import Vocab


forcy.set_extensions()
documents = [Doc(Vocab()).from_disk(p) for p in pathlib.Path("tests/docs").glob("*")]


@pytest.mark.parametrize("doc", documents)
def test_graph_underscore(doc):
    assert isinstance(doc._.nxgraph(), Graph)
