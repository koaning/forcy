<img src="icon.png" width=125 height=125 align="right">

# forCy

This small project contains support for (force directed layout) visualisations
for spaCy doc-objects. It's similar to displacy but it's slightly more interactive.

That's only part of "why the name" though. The main goal here is that this 
might also help you "for see" patterns for a dependency matcher. 


## Usage: 

```python
import spacy 

nlp = spacy.load("en_core_web_md")
doc = nlp("this is a single document")

doc._._nxgraph # returns you a networkx graph 
doc._.plot_force()
doc._.interactive_graph()
fdoc = Forcy(doc)

query
```
