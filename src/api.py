"""Small REST API for text summarization."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .summarizer import summarize_text, text_statistics

app = FastAPI(title='Automatic Document Summarization API', version='1.0.0')

class SummaryRequest(BaseModel):
    text: str = Field(min_length=1, max_length=200000)
    ratio: float = Field(default=0.25, gt=0, le=1)
    max_sentences: int | None = Field(default=None, ge=1, le=500)

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'document-summarization'}

@app.post('/summarize')
def summarize(request: SummaryRequest):
    try:
        summary = summarize_text(request.text, request.ratio, request.max_sentences)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        'summary': summary,
        'original_statistics': text_statistics(request.text),
        'summary_statistics': text_statistics(summary),
    }
