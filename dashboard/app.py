from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from src.summarizer import summarize_text, text_statistics
from src.document_reader import read_document, SUPPORTED_EXTENSIONS

st.set_page_config(page_title='DocuBrief NLP', page_icon='📄', layout='wide')
st.title('DocuBrief NLP')
st.caption('Automatic document summarization using extractive NLP')
mode = st.radio('Input method', ['Paste text', 'Upload document'], horizontal=True)
text = ''
if mode == 'Paste text':
    text = st.text_area('Original document', height=300, placeholder='Paste a document here...')
else:
    uploaded = st.file_uploader('Choose TXT, PDF or DOCX', type=['txt', 'pdf', 'docx'])
    if uploaded:
        suffix = Path(uploaded.name).suffix.lower()
        if suffix == '.txt':
            text = uploaded.getvalue().decode('utf-8', errors='replace')
        else:
            temp = Path('data/raw') / uploaded.name
            temp.parent.mkdir(parents=True, exist_ok=True)
            temp.write_bytes(uploaded.getvalue())
            try:
                text = read_document(temp)
            finally:
                temp.unlink(missing_ok=True)
ratio = st.slider('Summary length (% of sentences)', min_value=10, max_value=80, value=25, step=5) / 100
max_sentences = st.number_input('Maximum sentences (0 = no extra limit)', min_value=0, max_value=100, value=0)
if st.button('Generate summary', type='primary'):
    if not text.strip():
        st.warning('Enter or upload a document first.')
    else:
        try:
            summary = summarize_text(text, ratio, max_sentences or None)
            left, right = st.columns(2)
            with left:
                st.subheader('Original document')
                st.write(text)
            with right:
                st.subheader('Generated summary')
                st.write(summary)
                st.download_button('Download summary (.txt)', summary, file_name='summary.txt', mime='text/plain')
            a, b, c = st.columns(3)
            original = text_statistics(text)
            reduced = text_statistics(summary)
            a.metric('Original words', original['words'])
            b.metric('Summary words', reduced['words'])
            c.metric('Word reduction', f"{(1 - reduced['words'] / original['words']) * 100:.1f}%" if original['words'] else '0%')
            st.info('This is extractive summarization: selected sentences are taken from the source, not newly invented.')
        except Exception as exc:
            st.error(f'Could not summarize the document: {exc}')
