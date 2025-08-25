# Log Analyzer

A Python CLI to count requests per IP from large server logs and export results to CSV.

- Input: CSV with a `client_ip` column (e.g., `app_logs.csv`) or plain text logs where the first token is an IP.
- Output CSV columns: `ip,count,top_5` (sorted by count desc, ip asc).

## Quick start

Requirements: Python 3.9+

Run against the provided `app_logs.csv`:

```bash
python3 log_analyzer.py \
  --input app_logs.csv \
  --output results.csv \
  --top 5
```

Options:
- `--ip-column` to use a different CSV column name (default: `client_ip`).
- `--format csv|text|auto` to override format detection (default: auto).
- `--delimiter` for output CSV delimiter (default: `,`).
- `--no-header` to omit header row.
- `--quiet` to reduce stderr progress.

The script prints the Top-N summary to stdout and writes the full per-IP counts to the output CSV.