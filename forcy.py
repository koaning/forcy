import pathlib
import uuid
from string import Template

from IPython.core.display import HTML


def flatten(l):
    """Flattens a list."""
    return [item for sublist in l for item in sublist]


def doc_to_graph_json(doc):
    """Takes a spaCy doc and returns a dictionary. Useful for plotting."""
    nodes = [{"id": str(t.idx), "name": t.text, "pos": t.pos_, "group": t.pos_} for t in doc]
    translator = {t.idx: i for i, t in enumerate(doc)}
    nested_links = [[{'source': str(t.idx), 'target': str(r.idx), 'value': 1} for r in list(t.children)] for t in doc]
    return {"nodes": nodes, "links": flatten(nested_links)}


def create_javascript(data_dict):
    """Generates proper javascript code for a given data-dictionary."""
    div_id = "rando" + str(uuid.uuid4())[:8]
    html = Template('''<div id='$div_id'></div><script>$script</script>''')
    js_template = Template(pathlib.Path("graph.js").read_text())
    script = js_template.safe_substitute({'div_id': div_id, **data_dict})
    return html.safe_substitute({'script': script, 'div_id': div_id})


def render_graph(doc, width=700, height=450, filename=None):
    """
    Renders a proper force-directed layout that visualizes a spaCy document.

    Arguments:
        doc: spaCy document
        width: the width of the visualisation
        height: the height of the visualisation
        filename: filename to write generated html to
    """
    graph = doc_to_graph_json(doc)
    css = pathlib.Path("graph.css").read_text()
    styles = f"<style>{css}</style>"
    # https://bl.ocks.org/pstuffa/3393ff2711a53975040077b7453781a9
    dependency = '<script src="https://d3js.org/d3.v4.min.js"></script><script src="//d3js.org/d3-scale-chromatic.v0.3.min.js"></script>'
    draw = create_javascript({'data': graph, 'width': width, 'height': height})
    if filename:
        p = pathlib.Path(filename)
        if p.exists():
            p.unlink()
        p.write_text(styles + dependency + draw)
    return HTML(styles + dependency + draw)


if __name__ == "__main__":
    import spacy
    from forcy import render_graph, doc_to_graph_json

    nlp = spacy.load("en_core_web_sm")
    render_graph(nlp("Give me a recipe."), filename="index.html")