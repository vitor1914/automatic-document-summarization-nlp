from pathlib import Path
import pytest
from src.pipeline import summarize_file

def test_summarize_txt_file(tmp_path: Path):
    file = tmp_path / 'sample.txt'
    file.write_text('Water is essential for life. Water systems need maintenance. Monitoring prevents waste. Water systems need careful monitoring.', encoding='utf-8')
    result = summarize_file(file, ratio=0.5)
    assert result['filename'] == 'sample.txt'
    assert result['summary']
    assert result['original_statistics']['words'] > result['summary_statistics']['words']

def test_unsupported_file(tmp_path: Path):
    file = tmp_path / 'sample.csv'
    file.write_text('a,b', encoding='utf-8')
    with pytest.raises(ValueError):
        summarize_file(file)
