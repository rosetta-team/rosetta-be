import spacy

class DescriptionComparer:
    def __init__():
        self.nlp = spacy.load('en_core_web_lg')

    def compare(description1, description2):
        doc1 = self.nlp(description1)
        doc2 = self.nlp(description2)

        return doc1.similarity(doc2)
