# Automatic Document Summarization NLP

[Português](#português) | [English](#english)

## Português

Projeto de Processamento de Linguagem Natural (NLP) para resumir documentos automaticamente usando sumarização extrativa. O sistema seleciona frases representativas do texto original com TF-IDF e similaridade de cosseno, mantendo a ordem das frases selecionadas.

### Funcionalidades
- Entrada por texto ou arquivos TXT, PDF e DOCX.
- Ajuste da proporção do resumo e limite opcional de frases.
- Dashboard interativo com comparação entre original e resumo.
- Download do resumo em TXT.
- API REST com FastAPI.
- Estatísticas de caracteres, palavras, frases e redução de palavras.
- Testes com pytest e integração contínua via GitHub Actions.

### Requisitos
Python 3.10 ou superior.

### Instalação no Ubuntu / VS Code

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Executar dashboard

```bash
streamlit run dashboard/app.py
```

### Executar API

```bash
uvicorn src.api:app --reload
```

Abra `http://127.0.0.1:8000/docs` para testar a API. Endpoint principal: `POST /summarize` com JSON contendo `text`, `ratio` opcional e `max_sentences` opcional.

### Testes

```bash
pytest -q
```

### Limitações
A abordagem é extrativa: seleciona frases existentes, não cria paráfrases. A qualidade depende do texto e da segmentação. PDFs digitalizados como imagem precisam de OCR, que não está incluído.

## English

An NLP project that automatically summarizes documents using extractive summarization. It ranks sentences with TF-IDF vectors and cosine similarity, selects representative sentences, and preserves their original order.

### Features
- Text input or TXT, PDF, and DOCX files.
- Adjustable summary ratio and optional sentence limit.
- Interactive dashboard comparing source text and summary.
- Download summaries as TXT.
- REST API powered by FastAPI.
- Character, word, sentence, and word-reduction statistics.
- Pytest suite and GitHub Actions CI.

### Requirements
Python 3.10 or newer.

### Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run the dashboard

```bash
streamlit run dashboard/app.py
```

### Run the API

```bash
uvicorn src.api:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API. The main endpoint is `POST /summarize`, accepting `text`, optional `ratio`, and optional `max_sentences`.

### Tests

```bash
pytest -q
```

### Limitations
This is an extractive method: it selects existing sentences instead of generating paraphrases. Quality depends on the source text and sentence segmentation. OCR for scanned PDFs is not included.
