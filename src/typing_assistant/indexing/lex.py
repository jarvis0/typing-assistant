import math
from typing import Dict, List

from .collector import Collection
from .indexer import InvertedIndex, Posting


class WordLexicon:

    def __init__(self, total_frequency: int, inverse_term_frequency: float, postings: List[Posting]):
        self.tot_freq: int = total_frequency
        self.idf: float = inverse_term_frequency
        self.postings: List[Posting] = postings

    def __repr__(self) -> str:
        return f'$tot_freq: {self.tot_freq} - idf: {self.idf} - postings: {self.postings}$'


class Lexicon:

    def __init__(self):
        self.lexicon: Dict[str, WordLexicon] = {}

    def __add_word_lexicon(self, collection_size: int, term: str, postings: List[Posting]):
        self.lexicon[term] = WordLexicon(
            sum(p.frequency for p in postings),
            math.log((collection_size + 1) / len(postings)),
            postings,
        )

    def build_lexicon(self, collection: Collection, inv_index: InvertedIndex):
        collection_size = collection.get_size()
        for term, postings in inv_index.get_items():
            self.__add_word_lexicon(collection_size, term, postings)

    def get_words_lexicon(self) -> List[WordLexicon]:
        return self.lexicon.values()

    def get_word_lexicon(self, word: str) -> WordLexicon:
        return self.lexicon[word]
