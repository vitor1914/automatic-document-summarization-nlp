"""End-to-end document summarization pipeline."""
from pathlib import Path
from .document_reader import read_document
from .summarizer import summarize_text, text_statistics

def summarize_file(path: str | Path, ratio: float = 0.25, max_sentences: int | None = None) -> dict:
    text = read_document(path)
    summary = summarize_text(text, ratio=ratio, max_sentences=max_sentences)
    original_stats = text_statistics(text)
    summary_stats = text_statistics(summary)
    reduction = 0.0 if original_stats['words'] == 0 else round(
        100 * (1 - summary_stats['words'] / original_stats['words']), 2
    )
    return {
        'filename': Path(path).name,
        'original_text': text,
        'summary': summary,
        'original_statistics': original_stats,
        'summary_statistics': summary_stats,
        'word_reduction_percent': reduction,
    }
