# Movie Recommendation System (Basic)

A simple CLI that reads a CSV of movies and returns the top-N highest‑rated movies for a user-entered genre.

## Quick start

Prereqs
- Python 3.9+ (works on macOS, Linux, Windows)
- Dependencies: pandas, pyarrow (optional accelerator), pytest (tests), pylint (lint)

Setup (zsh)
```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest  # if you plan to run tests
```

Run the CLI
```zsh
python movie_recommender.py --csv movies.csv --limit 5
```
Notes
- `--csv` defaults to `movies.csv` in the repo root.
- Enter a genre when prompted (e.g., Action, Drama, Comedy). Use `q` to quit.

Run tests
```zsh
python -m pytest -q
```

Optional lint
```zsh
pylint movie_recommender.py
```

## Current folder structure
```
movie_recommender.py          # main CLI and logic (includes MovieDataIO class)
movies.csv                    # sample dataset (≥ 20 rows)
test_movie_recommender.py     # pytest unit tests
requirements.txt              # runtime deps (pandas, pyarrow, pylint)
pyproject.toml                # pytest/pylint config
functional-requirements.md    # functional spec
```

## Data schema
Required CSV columns:
- `title` (string)
- `genre` (string)
- `rating` (float)
- `year_release` (int)
- `language` (string)
- `director` (string)

Validation and cleaning
- Header row required; at least 20 data rows (pre‑clean).
- Strings are trimmed; `genre` is compared case‑insensitively.
- `rating` and `year_release` are coerced to numeric; invalid values are dropped.

## Behavior
- Case‑insensitive genre matching.
- Sort by `rating` desc, then `title` asc; return up to top 5.
- If fewer than 5 matches exist, prints available matches and a notice.
- Friendly messages for file not found, missing columns, insufficient rows, etc.
