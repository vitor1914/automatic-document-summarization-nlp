-- Optional persistence schema for storing document runs in SQLite.
CREATE TABLE IF NOT EXISTS summarization_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    original_word_count INTEGER NOT NULL,
    summary_word_count INTEGER NOT NULL,
    reduction_percent REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
