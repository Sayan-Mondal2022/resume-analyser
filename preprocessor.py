import spacy

nlp = spacy.load("en_core_web_sm")


def extract_keywords(text: str) -> set[str]:
    doc = nlp(text)

    keywords = set()

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN", "ADJ"]:
            keywords.add(token.lemma_.lower())

    return keywords


def extract_phrases(text: str) -> list[str]:
    doc = nlp(text)

    phrases = []
    phrases = [
        chunk.text.lower() for chunk in doc.noun_chunks if len(chunk.text.split()) > 1
    ]

    return phrases
