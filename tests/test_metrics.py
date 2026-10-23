import pytest
from src.summarizer import summarize_text, split_sentences, text_statistics

def test_split_sentences():
    assert split_sentences('First sentence. Second sentence!') == ['First sentence.', 'Second sentence!']

def test_summary_is_from_original_sentences():
    text = 'Water is essential for life. Water systems need maintenance. The moon orbits Earth. Water systems need careful monitoring.'
    summary = summarize_text(text, ratio=0.5)
    assert summary
    assert all(sentence in text for sentence in split_sentences(summary))

def test_empty_text():
    assert summarize_text('') == ''

def test_invalid_ratio():
    with pytest.raises(ValueError):
        summarize_text('Some text. More text.', ratio=0)

def test_statistics():
    stats = text_statistics('Water is vital. Water is useful.')
    assert stats['sentences'] == 2
    assert stats['words'] == 6
