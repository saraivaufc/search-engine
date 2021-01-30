import hashlib
import math
import string

import nltk

from models import Document, Word

nltk.download('punkt')
nltk.download('stopwords')

STOP_WORDS = set(nltk.corpus.stopwords.words("english"))


class TextProcessor(object):
    def hash(self, text):
        hash_object = hashlib.md5(text.encode('utf-8'))
        return hash_object.hexdigest()

    def convert_case(self, text):
        return text.lower()

    def remove_digits(self, text):
        return text.translate(str.maketrans('', '', string.digits))

    def remove_hyphens(self, text: str):
        return text.translate(str.maketrans('', '', '-'))

    def remove_punctuation(self, text: str):
        return text.translate(
            str.maketrans('', '', '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'))

    def word_extraction(self, text: str):
        document = text.replace("  ", " ").split(" ")
        return document

    def remove_stopwords(self, document: list):
        filtered_document = [w for w in document if not w in STOP_WORDS]
        return filtered_document

    def tokenize(self, text: str):
        sentence = self.convert_case(text)
        sentence = self.remove_digits(sentence)
        sentence = self.remove_punctuation(sentence)
        sentence = self.remove_hyphens(sentence)

        document = self.word_extraction(sentence)
        document = self.remove_stopwords(document=document)
        return document

    def calc_tf(self, word: Word, document: Document):
        return document.words.count(word.text) / len(document.words)

    def calc_idf(self, word: Word):
        documents_count = Document.objects().count()
        documents_occur = len(word.documents)
        return math.log(documents_count / (documents_occur + 0.0001))

    def calc_weight(self, word: Word, document: Document):
        idf = self.calc_idf(word)
        tf = self.calc_tf(word, document)
        return idf * tf

    def calc_sim(self, document, query_document):
        sum_weight_word_in_document_multiply_word_in_query = 0
        sum_weight_word_in_document_pow2 = 0
        sum_weight_word_in_query_pow2 = 0

        for word in query_document.words:
            query_word = Word.objects(text=word).first()
            if not query_word:
                continue

            weight_word_in_document = self.calc_weight(query_word,
                                                       document)

            weight_word_in_query = self.calc_weight(query_word,
                                                    query_document)

            sum_weight_word_in_document_multiply_word_in_query += \
                weight_word_in_document * weight_word_in_query

            sum_weight_word_in_document_pow2 += weight_word_in_document ** 2
            sum_weight_word_in_query_pow2 += weight_word_in_query ** 2

        sim = sum_weight_word_in_document_multiply_word_in_query / (
                (math.sqrt(sum_weight_word_in_document_pow2) * math.sqrt(
                    sum_weight_word_in_query_pow2)) + 0.0001
        )

        return sim
