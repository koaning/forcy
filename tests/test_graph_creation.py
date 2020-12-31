import pathlib

import pytest
from forcy import Forcy

from spacy.tokens import Doc
from spacy.vocab import Vocab

documents = [Doc(Vocab()).from_disk(p) for p in pathlib.Path("tests/docs").glob("*")]


@pytest.mark.parametrize("doc", documents)
def test_init(doc):
    fdoc = Forcy(doc)
    assert len(fdoc.graph.nodes) == len(doc)
