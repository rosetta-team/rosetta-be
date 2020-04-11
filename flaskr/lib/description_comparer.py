import spacy

class DescriptionComparer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.nlp.Defaults.stop_words |= {'Array', 'prototype', }

    def convert_special_chars(self, word):
        conversion_dict = {
            '<<':'push',
            '&':'intersection',
            '+':'concat',
            '-':'splice',
            '*':'join',
            '<=>':'find',
            '==':'equals',
            '[]':'find',
            '#':' '
        }

        special_symbols = conversion_dict.keys()
        for symbol in special_symbols:
            if symbol in word:
                word.replace(symbol, conversion_dict[symbol])

        return word


    def compare(self, description1, description2):
        doc1 = self.nlp(description1)
        doc2 = self.nlp(description2)

        return doc1.similarity(doc2)
