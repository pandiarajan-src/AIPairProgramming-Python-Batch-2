"""Movie Recommendation System (Basic) — Single-file program.

- Contains the CLI entrypoint and all supporting logic.
- I/O methods are encapsulated in the `MovieDataIO` class.

Usage:
    python -m src.main [--csv PATH]
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

import pandas as pd


# -----------------------------
# Data / I/O layer
# -----------------------------

REQUIRED_COLUMNS = {
    "title",
    "genre",
    "rating",
    "year_release",
    "language",
    "director",
}


@dataclass
class LoadResult:
    """Result of loading and cleaning the movies CSV."""

    dataframe: pd.DataFrame
    dropped_non_numeric_rating: int
    dropped_missing_required: int
    raw_row_count: int


class MovieDataIO:
    """Encapsulates reading and validating the movies CSV file."""

    def _validate_file_exists(self, csv_path: Path) -> None:
        if not csv_path.exists():
            raise FileNotFoundError(
                (
                    f"Could not find CSV at {csv_path}. "
                    "Provide a valid path or place the file at movies.csv."
                )
            )

    @staticmethod
    def _validate_required_columns(df: pd.DataFrame) -> None:
        # Use lowercase for robust checks
        columns_lower = set(map(str.lower, df.columns))
        missing = REQUIRED_COLUMNS - columns_lower
        if missing:
            base = (
                "CSV must contain columns: title, genre, rating, year_release, language, director."
            )
            msg = (
                f"{base} Missing: {sorted(missing)}. " f"Found: {sorted(columns_lower)}"
            )
            raise ValueError(msg)

    def load_and_clean(self, csv_path: Path) -> LoadResult:
        """Load, validate, and clean the movies dataset.

        Steps:
        - Load CSV with pandas.
        - Validate required columns are present.
        - Validate at least 20 data rows (pre-cleaning).
        - Clean: trim strings, normalize genre, coerce numerics, drop invalid rows.
        """

        self._validate_file_exists(csv_path)
        try:
            df = pd.read_csv(csv_path)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to parse CSV: {exc}") from exc

        raw_row_count = len(df)
        if raw_row_count < 20:
            raise ValueError(
                f"CSV must contain at least 20 data rows; found {raw_row_count}."
            )

        # Normalize column names to lowercase for consistency
        df = df.rename(columns=str.lower)
        self._validate_required_columns(df)

        before_clean = len(df)

        # Trim text fields
        for col in ("title", "genre", "language", "director"):
            df[col] = df[col].astype(str).str.strip()

        # Normalize genre for filtering
        df["genre_norm"] = df["genre"].str.lower()

        # Coerce numerics
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df["year_release"] = (
            pd.to_numeric(df["year_release"], errors="coerce").astype("Int64")
        )

        # Count rows that will be dropped due to rating not numeric
        dropped_non_numeric_rating = df["rating"].isna().sum()

        # Drop rows with missing required values (title/genre/rating/year_release)
        df = df.dropna(subset=["title", "genre", "rating", "year_release"]).copy()
        # Remove rows where title/genre are empty after trim
        df = df[(df["title"] != "") & (df["genre"] != "")]

        dropped_missing_required = before_clean - len(df)

        return LoadResult(
            dataframe=df,
            dropped_non_numeric_rating=int(dropped_non_numeric_rating),
            dropped_missing_required=int(dropped_missing_required),
            raw_row_count=int(raw_row_count),
        )


# -----------------------------
# Recommendation logic
# -----------------------------

def top_n_by_genre(df: pd.DataFrame, genre: str, n: int = 5) -> pd.DataFrame:
    """Return up to N highest-rated movies for a given genre.

    - Match is case-insensitive against `genre_norm` if present, else lowercased `genre`.
    - Sort by rating desc, then title asc for stable ordering.
    - Returns a new DataFrame with relevant columns preserved.
    """

    if not isinstance(df, pd.DataFrame):  # defensive
        raise TypeError("df must be a pandas DataFrame")

    if not isinstance(genre, str) or not genre.strip():
        return df.iloc[0:0]  # empty selection

    norm = genre.strip().lower()

    if "genre_norm" in df.columns:
        mask = df["genre_norm"] == norm
    else:
        mask = df["genre"].astype(str).str.lower() == norm

    filtered = df.loc[mask].copy()
    if filtered.empty:
        return filtered

    ordered = filtered.sort_values(by=["rating", "title"], ascending=[False, True])
    return ordered.head(n)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the application."""
    parser = argparse.ArgumentParser(
        description="Movie Recommendation System (Basic)"
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("movies.csv"),
        help="Path to the movies CSV (default: movies.csv)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of results to show (default: 5)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entrypoint for the CLI; returns a process exit code."""
    args = parse_args(argv)

    # Load and validate dataset
    try:
        io = MovieDataIO()
        result = io.load_and_clean(args.csv)
    except (FileNotFoundError, ValueError) as exc:  # user-friendly early failure
        print(f"Error: {exc}")
        return 2

    df = result.dataframe
    if result.dropped_non_numeric_rating:
        print(
            "Warning: Dropped "
            f"{result.dropped_non_numeric_rating} row(s) due to non-numeric rating."
        )
    if result.dropped_missing_required:
        print(
            "Warning: Dropped "
            f"{result.dropped_missing_required} row(s) due to missing required fields."
        )

    print("Type a genre to get recommendations (or 'q' to quit). Examples: Action, Drama, Comedy")
    while True:
        try:
            user_input = input("Enter a genre (or 'q' to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return 0

        if user_input.lower() in {"q", "quit"}:
            print("Goodbye!")
            return 0

        if not user_input:
            print("Please enter a non-empty genre.")
            continue

        recs = top_n_by_genre(df, user_input, n=max(1, args.limit))
        if recs.empty:
            print(f"No matches found for genre '{user_input}'. Try another genre.")
            continue

        count = len(recs)
        if count < args.limit:
            suffix = "match" if count == 1 else "matches"
            print(f"Only {count} {suffix} found.")

        for rank, row in enumerate(
            recs.reset_index(drop=True).itertuples(index=False), start=1
        ):
            # Access by attribute names matching columns
            title = getattr(row, "title", "<unknown>")
            genre = getattr(row, "genre", "<unknown>")
            rating = getattr(row, "rating", "<na>")
            year = getattr(row, "year_release", "<na>")
            print(f"{rank}. {title} — {genre} — rating: {rating} — year: {year}")


if __name__ == "__main__":
    sys.exit(main())
