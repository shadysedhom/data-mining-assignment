from typing import Optional
from sklearn.feature_extraction.text import CountVectorizer

def make_unigram_vectorizer(min_occurrences: int = 2, max_features: Optional[int] = None, stop_words: Optional[str] = "english", lowercase: bool = True):
	return CountVectorizer(
		lowercase=lowercase,
		ngram_range=(1, 1),
		min_df=min_occurrences,
		max_features=max_features,
		stop_words=stop_words,
	)


def make_unigram_bigram_vectorizer(min_occurrences: int = 2, max_features: Optional[int] = None, stop_words: Optional[str] = "english", lowercase: bool = True):
	return CountVectorizer(
		lowercase=lowercase,
		ngram_range=(1, 2),
		min_df=min_occurrences,
		max_features=max_features,
		stop_words=stop_words,
	)
