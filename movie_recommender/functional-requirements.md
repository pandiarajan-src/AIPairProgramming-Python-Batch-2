# Movie Recommendation System (Basic) — Functional Requirements

## Objective
Build a small CLI program that, given a CSV of movies (`title`, `genre`, `rating`, `year_release`, `language`, `director`), lets a user enter a genre and returns the top 5 highest‑rated movies in that genre, handling cases with fewer than 5 matches gracefully.

## In Scope
- Read and validate a CSV file (≥ 20 data rows) with columns: `title`, `genre`, `rating`, `year_release`, `language`, `director`
- Use Pandas for parsing, filtering, sorting, and simple data cleaning.
- CLI prompts for user input (genre) and user-friendly outputs.
- Basic error handling for malformed data and common runtime issues.

## Out of Scope (for this iteration)
- Web UI, APIs, or databases.
- Advanced recommendations (collaborative/content-based filtering).
- Multi-genre queries or fuzzy/similarity matching beyond case-insensitive equality.

## Data Specification
- File: `data/movies.csv` (path configurable via CLI flag or env var if desired).
- Header row required.
- Minimum 20 data rows (excluding header). Validation must fail with a helpful message if fewer.
- Columns (required):
  - `title` (string, non-empty after trim)
  - `genre` (string, non-empty after trim)
  - `rating` (numeric float; suggested scale 0.0–10.0; 
  - `year_release` (numeric int; non-empty)
  - `language` (string, non-empty after trim)
  coerce non-numeric to NaN and drop those rows with a warning)

### Data Cleaning Rules
- Trim leading/trailing whitespace for `title` and `genre`.
- Standardize `genre` for matching: compare on lowercase value.
- Coerce `rating` to numeric (Pandas `to_numeric(..., errors='coerce')`), drop rows with missing or NaN `rating`.
- Drop rows missing required columns or with empty `title`/`genre` after trimming.

## User Interaction (CLI Flow)
1. On start, load and validate the CSV. Show a clear error if validation fails (file missing, bad columns, <20 rows, etc.).
2. Prompt: "Enter a genre (or 'q' to quit): "
3. When a genre is entered (case-insensitive):
   - Filter movies where `genre` equals the entered genre after normalization.
   - Sort by `rating` descending; break ties by `title` ascending.
   - Display up to 5 results with rank, title, genre (original case), and rating.
   - If 0 results, display a friendly message and re-prompt.
   - If <5 results, display available results and message: "Only N match(es) found."
4. Repeat until the user enters `q`/`quit`.

## Functional Requirements
- FR-1 CSV Loading: The system shall load a CSV file path (default `data/movies.csv`).
- FR-2 Column Validation: The system shall validate presence of `title`, `genre`, `rating` columns; otherwise exit with a clear error.
- FR-3 Row Count Validation: The system shall validate the CSV has ≥ 20 data rows (excluding header); otherwise exit with a clear error.
- FR-4 Data Cleaning: The system shall trim `title`/`genre`, coerce `rating` to float, and drop rows that are invalid per Data Cleaning Rules.
- FR-5 Genre Input: The system shall prompt for a genre and accept case-insensitive input; `q`/`quit` exits.
- FR-6 Filtering: The system shall filter rows whose normalized `genre` equals the normalized user input.
- FR-7 Sorting: The system shall sort matches by `rating` desc, then `title` asc.
- FR-8 Limiting: The system shall return up to the top 5 matches.
- FR-9 Fewer-than-5 Handling: If <5 matches, the system shall display available results and an informative message.
- FR-10 No-Match Handling: If 0 matches, the system shall inform the user and re-prompt.
- FR-11 Errors: The system shall provide user-friendly messages for: file not found, malformed CSV, missing columns, insufficient rows, and non-numeric ratings.

## Non-Functional Requirements (Minimal)
- Runtime: Python 3.9+.
- Dependencies: `pandas` (latest stable 1.x/2.x compatible with chosen Python), `pyarrow` optional for faster CSV.
- Performance: Designed for small CSVs (hundreds to low thousands of rows) and completes operations in <1s on typical hardware.
- Portability: Works on macOS, Linux, Windows.

## Implementation Notes (Pandas)
- Prefer Pandas for CSV parsing and transformation.
- Typical operations to leverage IDE autocompletion for filtering and sorting:

```python
import pandas as pd

# Load
df = pd.read_csv("data/movies.csv")

# Validate columns
required = {"title", "genre", "rating"}
missing = required - set(df.columns.str.lower())
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

# Normalize and clean
df = df.rename(columns=str.lower)
df["title"] = df["title"].astype(str).str.strip()
df["genre"] = df["genre"].astype(str).str.strip()
df["genre_norm"] = df["genre"].str.lower()
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df = df.dropna(subset=["title", "genre", "rating"])  # drop invalid

# Example query
query_genre = "Action"
result = (
    df[df["genre_norm"] == query_genre.strip().lower()]
      .sort_values(by=["rating", "title"], ascending=[False, True])
      .head(5)
)
```

## Error Handling Guidelines
- File not found: "Could not find CSV at <path>. Provide a valid path or place the file at data/movies.csv."
- Bad columns: "CSV must contain columns: title, genre, rating. Found: <list>."
- Insufficient rows: "CSV must contain at least 20 data rows; found <n>."
- Non-numeric ratings: Coerce to NaN; drop those rows; log count dropped.
- Unexpected: Show concise error and exit with non-zero code.

## Output Format
- For each result row, print: `<rank>. <title> — <genre> — rating: <rating>`
- After printing results, prompt for another genre until user quits.

## Acceptance Criteria
1. Given a valid CSV (≥20 rows) and a genre with >5 matches, the program prints exactly 5 titles sorted by rating desc, title asc.
2. Given a valid CSV and a genre with exactly 5 matches, the program prints those 5 titles in the correct order.
3. Given a valid CSV and a genre with <5 matches, the program prints only the existing matches and a message: "Only N match(es) found."
4. Given a valid CSV and a genre with 0 matches, the program prints a "No matches found" message and re-prompts.
5. Given a CSV missing required columns, the program exits with a clear error.
6. Given a CSV with <20 rows, the program exits with a clear error.
7. Given a CSV with some non-numeric ratings, those rows are dropped and the rest operate normally; a warning is shown.

## File/Folder Layout (proposed)
- `data/movies.csv` — input data (≥ 20 data rows)
- `src/main.py` — CLI entry point
- `src/io.py` — CSV load/validation helpers
- `src/recommend.py` — filtering/sorting logic
- `README.md` — setup and usage

## Future Enhancements (nice-to-have)
- Allow multiple genres or partial matches.
- Support interactive suggestions (list available genres) once data is loaded.
- Add unit tests (pytest) and simple CI.
- Optionally export results as JSON.
