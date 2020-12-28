def flatten(l):
    """Flattens a list"""
    return [item for sublist in l for item in sublist]

def doc_to_graph_json(doc):
    """Takes a spaCy doc and returns a dictionary. Useful for plotting."""
    nodes = [{"idx": t.idx, "name": t.text, "pos": t.pos_, "group": 1} for t in doc]
    translator = {t.idx: i for i, t in enumerate(doc)}
    nested_links = [[{'source': translator[t.idx], 'target': translator[r.idx], 'weight': 1} for r in list(t.children)] for t in doc]
    return {"nodes": nodes, "links": flatten(nested_links)}

def create_javascript(data_dict):
    """Generates proper javascript code for a given data-dictionary."""
    html = Template('''<div id='maindiv'></div><script>$script</script>''')
    js_template = Template(pathlib.Path("graph.js").read_text())
    script = js_template.safe_substitute(data_dict)
    return html.safe_substitute({'script': script})

def render_graph(doc, width=500, height=300):
    """
    Renders a proper force-directed layout that visualizes a spaCy document.

    Arguments:
        width: the width of the visualisation
        height: the height of the visualisation
    """
    graph = doc_to_graph_json(doc)
    css = pathlib.Path("graph.css").read_text()
    styles = f"<style>{css}</style>"
    dependency = '<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.3.0/d3.min.js"></script>'
    draw = create_javascript({'data': graph, 'width': width, 'height': height})
    return HTML(styles + dependency + draw)
