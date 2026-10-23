"""Extractive summarization using sentence-level TF-IDF similarity."""
from __future__ import annotations
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+')

def split_sentences(text: str) -> list[str]:
    """Split text into plausible sentences, ignoring empty pieces."""
    cleaned = re.sub(r'\s+', ' ', text or '').strip()
    if not cleaned:
        return []
    return [s.strip() for s in _SENTENCE_SPLIT.split(cleaned) if s.strip()]

def summarize_text(text: str, ratio: float = 0.25, max_sentences: int | None = None) -> str:
    """Return an extractive summary while preserving original sentence wording.

    The summary selects representative sentences and returns them in original order.
    It is not a generative model: output sentences are copied from the source text.
    """
    if not isinstance(text, str):
        raise TypeError('text must be a string')
    if not 0 < ratio <= 1:
        raise ValueError('ratio must be greater than 0 and at most 1')
    sentences = split_sentences(text)
    if len(sentences) <= 1:
        return text.strip()
    if ratio == 1 and max_sentences is None:
        return ' '.join(sentences)
    try:
        matrix = TfidfVectorizer(stop_words=None, ngram_range=(1, 2)).fit_transform(sentences)
        similarity = cosine_similarity(matrix, matrix)
        scores = similarity.sum(axis=1).ravel()
    except ValueError:
        scores = [len(s.split()) for s in sentences]
    count = max(1, round(len(sentences) * ratio))
    if max_sentences is not None:
        if max_sentences < 1:
            raise ValueError('max_sentences must be at least 1')
        count = min(count, max_sentences)
    chosen = sorted(sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:count])
    return ' '.join(sentences[i] for i in chosen)

def text_statistics(text: str) -> dict[str, int | float]:
    words = re.findall(r"\b[\w'-]+\b", text or '', flags=re.UNICODE)
    sentences = split_sentences(text or '')
    return {
        'characters': len(text or ''),
        'words': len(words),
        'sentences': len(sentences),
        'unique_words': len(set(w.casefold() for w in words)),
    }
