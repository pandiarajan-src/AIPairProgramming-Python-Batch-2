#!/usr/bin/env python3
"""
Server Log Analyzer

Reads a large server log and computes request counts per IP.
Supports CSV input (column 'client_ip' by default) and generic text logs
where the IP is the first whitespace-delimited token.

Outputs a CSV with columns: ip,count,top_5 (sorted count desc, ip asc),
and prints a top-N summary to stdout.

Exit codes:
  0 success
  2 input file not found/unreadable
  3 output path unwritable/parent not creatable
  4 unexpected I/O error
"""
from __future__ import annotations

import argparse
import csv
import ipaddress
import os
import sys
import time
from collections import defaultdict
from typing import Dict, Iterable, Tuple


def is_csv_path(path: str) -> bool:
    """Return True if the given path appears to be a CSV file by extension."""
    return path.lower().endswith(".csv")


def parse_args() -> argparse.Namespace:
    """Parse and return command-line arguments for the CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze server logs and count requests per IP"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to input log file (CSV or text)",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to output CSV (will contain ip,count,top_5)",
    )
    parser.add_argument(
        "--top",
        "-t",
        type=int,
        default=5,
        help="Number of top IPs to flag and print (default: 5)",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding for input (default: utf-8)",
    )
    parser.add_argument(
        "--delimiter",
        default=",",
        help="CSV delimiter for output (default: ,)",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Omit header row in output CSV",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress non-error output except top-N summary",
    )
    parser.add_argument(
        "--ip-column",
        default="client_ip",
        help="IP column name when reading CSV (default: client_ip)",
    )
    parser.add_argument(
        "--format",
        choices=["auto", "csv", "text"],
        default="auto",
        help="Input format detection override (default: auto)",
    )
    return parser.parse_args()


def validate_ip(token: str) -> bool:
    """Validate a token as an IPv4/IPv6 address using ipaddress."""
    try:
        ipaddress.ip_address(token)
        return True
    except ValueError:
        return False


def read_ips_from_csv(
    path: str, encoding: str, ip_column: str
) -> Iterable[Tuple[str, bool]]:
    """Yield pairs of (ip, is_valid) from a CSV file using the given column.

    is_valid is True if the IP parses, otherwise False. Malformed rows yield
    (token, False) so the caller can count and proceed.
    """
    with open(path, "r", encoding=encoding, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            # Empty or no header
            return
        if ip_column not in reader.fieldnames:
            raise ValueError(
                f"IP column '{ip_column}' not found in CSV header: {reader.fieldnames}"
            )
        for row in reader:
            ip = (row.get(ip_column) or "").strip()
            if not ip:
                yield (ip, False)
                continue
            yield (ip, validate_ip(ip))


def read_ips_from_text(path: str, encoding: str) -> Iterable[Tuple[str, bool]]:
    """Yield pairs of (ip, is_valid) from a text log by first token per line."""
    with open(path, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            # first token until whitespace
            first = s.split(None, 1)[0]
            yield (first, validate_ip(first))


def detect_format(path: str, fmt_opt: str) -> str:
    """Return the input format choice ('csv' or 'text'), respecting override."""
    if fmt_opt != "auto":
        return fmt_opt
    if is_csv_path(path):
        return "csv"
    return "text"


def ensure_output_parent(output_path: str) -> None:
    """Ensure the parent directory for output exists, creating it if needed."""
    parent = os.path.dirname(os.path.abspath(output_path))
    if not parent:
        return
    try:
        os.makedirs(parent, exist_ok=True)
    except OSError as e:
        raise PermissionError(
            f"Cannot create parent directory '{parent}': {e}"
        ) from e


def analyze(
    input_path: str,
    output_path: str,
    top_n: int,
    encoding: str,
    delimiter: str,
    no_header: bool,
    quiet: bool,
    ip_column: str,
    fmt_opt: str,
) -> int:
    """Analyze the input log and produce a CSV with per-IP counts.

    Returns an exit code consistent with the CLI contract.
    """
    # pylint: disable=too-many-arguments, too-many-locals, too-many-return-statements, too-many-branches, too-many-statements
    t0 = time.time()

    # Validate input file
    if not os.path.exists(input_path) or not os.path.isfile(input_path):
        print(f"Input file not found or not a file: {input_path}", file=sys.stderr)
        return 2

    # Determine reader
    fmt = detect_format(input_path, fmt_opt)
    if not quiet:
        print(f"Reading '{input_path}' as {fmt.upper()}...", file=sys.stderr)

    counts: Dict[str, int] = defaultdict(int)
    total_lines = 0
    malformed = 0

    try:
        if fmt == "csv":
            for ip, ok in read_ips_from_csv(input_path, encoding, ip_column):
                total_lines += 1
                if not ok:
                    malformed += 1
                    continue
                counts[ip] += 1
        else:
            for ip, ok in read_ips_from_text(input_path, encoding):
                total_lines += 1
                if not ok:
                    malformed += 1
                    continue
                counts[ip] += 1
    except ValueError as ve:
        print(str(ve), file=sys.stderr)
        return 2
    except PermissionError as pe:
        print(f"Permission error reading input: {pe}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"Unexpected error reading input: {e}", file=sys.stderr)
        return 4

    # Prepare top-N set
    # Sort by count desc, then ip asc
    sorted_items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    top = sorted_items[: max(0, top_n)]
    top_set = {ip for ip, _ in top}

    # Write output CSV
    try:
        ensure_output_parent(output_path)
        with open(output_path, "w", newline="", encoding="utf-8") as out:
            writer = csv.writer(out, delimiter=delimiter)
            if not no_header:
                writer.writerow(["ip", "count", "top_5"])
            for ip, count in sorted_items:
                writer.writerow([ip, count, str(ip in top_set).lower()])
    except PermissionError as pe:
        print(f"Cannot write output: {pe}", file=sys.stderr)
        return 3
    except OSError as e:
        print(f"Unexpected error writing output: {e}", file=sys.stderr)
        return 4

    # Print top-N summary to stdout
    print(f"Top {top_n} IPs:")
    for idx, (ip, cnt) in enumerate(top, start=1):
        print(f"{idx}. {ip} — {cnt}")

    # Final stats
    elapsed = time.time() - t0
    unique_ips = len(counts)
    if not quiet:
        print(
            f"Processed lines={total_lines}, unique_ips={unique_ips}, malformed_lines={malformed}, "
            f"elapsed={elapsed:.2f}s",
            file=sys.stderr,
        )
        if malformed:
            print(
                f"Warning: skipped {malformed} malformed line(s)", file=sys.stderr
            )

    return 0


def main() -> None:
    """Entry point for the CLI."""
    args = parse_args()
    rc = analyze(
        input_path=args.input,
        output_path=args.output,
        top_n=args.top,
        encoding=args.encoding,
        delimiter=args.delimiter,
        no_header=args.no_header,
        quiet=args.quiet,
        ip_column=args.ip_column,
        fmt_opt=args.format,
    )
    sys.exit(rc)


if __name__ == "__main__":
    main()
