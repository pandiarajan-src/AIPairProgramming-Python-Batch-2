from pathlib import Path

import pandas as pd
import pytest

from movie_recommender import MovieDataIO, top_n_by_genre


def write_csv(tmp_path: Path, rows):
    """Write a temporary CSV with the provided row strings; return the file path."""
    path = tmp_path / "movies.csv"
    header = "title,genre,rating,year_release,language,director\n"
    with path.open("w", encoding="utf-8") as f:
        f.write(header)
        for r in rows:
            f.write(r + "\n")
    return path


def gen_rows(n: int):
    """Generate n CSV row strings with Action genre and varying ratings."""
    base = (
        "Title{idx},Action,{rating},2019,English,Dir{idx}"
    )
    for i in range(n):
        yield base.format(idx=i, rating=7.0 + (i % 3))


def test_load_and_clean_validates_row_count(tmp_path: Path):
    """Fewer than 20 rows should raise a ValueError during validation."""
    path = write_csv(tmp_path, list(gen_rows(10)))
    io = MovieDataIO()
    with pytest.raises(ValueError):
        io.load_and_clean(path)


def test_load_and_clean_happy_path(tmp_path: Path):
    """A valid CSV (>=20 rows) loads and includes all required columns."""
    path = write_csv(tmp_path, list(gen_rows(25)))
    io = MovieDataIO()
    result = io.load_and_clean(path)
    df = result.dataframe
    assert {"title", "genre", "rating", "year_release", "language", "director"}.issubset(
        set(df.columns)
    )
    assert len(df) >= 20


def test_load_and_clean_coerces_rating(tmp_path: Path):
    """Non-numeric rating values are coerced to NaN and dropped."""
    rows = list(gen_rows(20))
    rows[0] = "BadRating,Action,not_a_number,2019,English,Someone"
    path = write_csv(tmp_path, rows)
    io = MovieDataIO()
    result = io.load_and_clean(path)
    assert result.dropped_non_numeric_rating >= 1


def test_top_n_returns_sorted_action():
    """Top-N for Action returns the highest ratings first and respects limit."""
    df = pd.DataFrame(
        [
            {"title": "A", "genre": "Action", "genre_norm": "action", "rating": 9.0},
            {"title": "B", "genre": "Action", "genre_norm": "action", "rating": 8.5},
            {"title": "C", "genre": "Drama",  "genre_norm": "drama",  "rating": 8.8},
            {"title": "D", "genre": "Action", "genre_norm": "action", "rating": 7.0},
        ]
    )
    res = top_n_by_genre(df, "Action", n=2)
    assert list(res["title"]) == ["A", "B"]


def test_top_n_handles_fewer_than_n():
    """When fewer than N matches exist, return only available rows."""
    df = pd.DataFrame(
        [
            {"title": "OnlyOne", "genre": "Drama", "genre_norm": "drama", "rating": 8.8}
        ]
    )
    res = top_n_by_genre(df, "Drama", n=5)
    assert len(res) == 1
    assert res.iloc[0]["title"] == "OnlyOne"


def test_top_n_no_matches():
    """No matches for a genre should return an empty DataFrame."""
    df = pd.DataFrame(
        [
            {"title": "A", "genre": "Action", "genre_norm": "action", "rating": 9.0}
        ]
    )
    res = top_n_by_genre(df, "Comedy", n=3)
    assert res.empty
