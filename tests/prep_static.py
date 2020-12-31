import spacy

nlp = spacy.load("en_core_web_md")

queries = [
    "Give me 5 penguins with a male gender and a weight less than 50",
    "Give me 3 penguins from the Torgersen island",
    "Give me 10 penguins with a flipper length less than 196 and a body mass over 3800",
]

for i, q in enumerate(queries):
    nlp(q).to_disk(f"tests/docs/doc{i+1}")