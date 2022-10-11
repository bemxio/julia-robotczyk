import spacy

# https://spacy.io/api/doc
# https://spacy.io/api/token
# https://universaldependencies.org/docs/pl/dep/

nlp = spacy.load("pl_core_news_sm")

text = "aha wez wyjdz idz pa"
doc = nlp(text)

for token in doc:
    print(token, token.dep_)