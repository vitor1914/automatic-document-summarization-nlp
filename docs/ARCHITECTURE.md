# Architecture

1. **Input:** plain text or TXT/PDF/DOCX documents.
2. **Extraction:** `src/document_reader.py` extracts text from supported file types.
3. **Summarization:** `src/summarizer.py` splits text into sentences, vectorizes them with TF-IDF, scores sentence similarity, selects representative sentences, and preserves their original order.
4. **Interfaces:** Streamlit dashboard (`dashboard/app.py`) and REST API (`src/api.py`).
5. **Quality:** pytest tests and GitHub Actions workflow.

The current approach is extractive. It does not paraphrase text and does not guarantee factual completeness. Scanned PDFs may require OCR, which is not included.
