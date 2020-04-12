import spacy

class DescriptionComparer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.nlp.Defaults.stop_words |= {'prototype', '(', ')', 'returns'}

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
            '#':' ',
             '.':' ',
             '::':' ',
             '_':' '
        }

        symbols = conversion_dict.keys()
        for symbol in symbols:
            if symbol in word:
                word = word.replace(symbol, conversion_dict[symbol])

        return word

    def preprocess_doc(self, text):
        self.break_camelcase(text)
        doc = self.nlp(text)
        filtered_doc = [word for word in doc if word.text not in self.nlp.Defaults.stop_words]
        return ' '.join(map(str, filtered_doc))

    def break_camelcase(self, text):
        for letter in text:
            if letter.isupper():
                text = text.replace(letter, f" {letter}")

        return text



    def compare(self, description1, description2):
        doc1 = self.nlp(self.convert_special_chars(self.preprocess_doc(description1)))
        doc2 = self.nlp(self.convert_special_chars(self.preprocess_doc(description2)))
        return doc1.similarity(doc2)
