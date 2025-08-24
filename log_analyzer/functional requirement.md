# Functional Requirements — Server Log Analyzer

## Objective
Implement a Python CLI script that analyzes a large web server access log to:
- Count the number of requests per IP address.
- Identify the top 5 IPs by request count (configurable N).
- Save the full per-IP counts to a CSV file.

## In Scope
- Single-file CLI written in Python 3.9+ (standard library only).
- Efficient streaming read of large files (line-by-line) without loading entire file into memory.
- IPv4 and IPv6 support.
- Tolerant of malformed lines (skip and continue).

Out of scope: distributed processing, remote log ingestion, log rotation handling, non-file inputs.

## Inputs
- Required: `--input / -i` path to a log file (e.g., `access.log`).
- Format: Common/Combined Log Format. The client IP is the first token in each line (up to first whitespace).
- Optional: `--encoding` (default `utf-8`).

## Outputs
- CSV file at path given by `--output / -o` with columns:
  - `ip` (string)
  - `count` (integer)
  - `top_5` (boolean; `true` if in the top N by count)
- Sort order in CSV: `count` desc, then `ip` asc.
- Stdout summary: top N list (rank, ip, count) after processing.

## Core Behavior
1. Open the input file with buffered IO; iterate line-by-line.
2. For each non-empty line:
   - Extract the first whitespace-delimited token.
   - Validate as IP using `ipaddress` module; if invalid, increment `malformed_lines` and continue.
   - Increment a counter for that IP.
3. After reading all lines:
   - Determine the top N IPs by count (default N=5).
   - Write CSV for all IPs with `top_5` marked `true` for those in top N.
   - Print a top-N summary to stdout.

## CLI Interface
- `python log_analyzer.py --input <path> --output <path> [--top N] [--encoding ENC] [--delimiter D] [--no-header] [--quiet]`
- Options:
  - `--input, -i` (required): path to input log.
  - `--output, -o` (required): path to CSV output (parent dir must exist or be creatable).
  - `--top, -t` (optional): N for top list/flag (default: 5).
  - `--encoding` (optional): file encoding (default: `utf-8`).
  - `--delimiter` (optional): CSV delimiter (default: `,`).
  - `--no-header` (optional): omit header row.
  - `--quiet, -q` (optional): suppress non-error logs; still print top-N.

## Error Handling & Exit Codes
- Input file not found/unreadable → exit 2, message to stderr.
- Output path unwritable/parent not creatable → exit 3, message to stderr.
- Unexpected IO errors → exit 4, message to stderr.
- Malformed lines are skipped and counted; warn to stderr at end if `malformed_lines > 0`.

## Performance
- Streaming read with O(U) memory, where U = unique IPs.
- Avoid expensive regex; only parse first token and validate with `ipaddress`.
- Suitable for multi-GB logs, bound by disk IO.

## Telemetry / Reporting
- At completion, print stats: total_lines, unique_ips, malformed_lines, elapsed_time.
- Optional periodic progress (every ~5–10M lines) unless `--quiet` is set.

## Acceptance Criteria
- Generates CSV with header `ip,count,top_5`, sorted by count desc then ip asc.
- Top-N in stdout matches CSV rows where `top_5` is `true`.
- Handles fewer than 5 unique IPs gracefully (flags all existing as top-N if applicable).
- Skips malformed lines without failing and reports the count.
- Returns exit code 0 on success and the specified non-zero codes on failure.

## Dependencies & Compatibility
- Python standard library only: `argparse`, `csv`, `ipaddress`, `collections`, `time`, `os`, `io`.
- Compatible with macOS/Linux.

## Deliverables
- `log_analyzer.py` implementing the above.
- `README.md` with usage and examples.
- Optional: small sample `access.log` and expected CSV for tests.
