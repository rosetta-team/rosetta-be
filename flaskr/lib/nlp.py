import spacy

class DescriptionComparer:
    def __init__(description1, description2):
        self.nlp = spacy.load('en_core_web_lg')
        self.doc1 = description1
        self.doc2 = description2
