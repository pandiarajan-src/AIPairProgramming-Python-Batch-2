"""Unit tests for log_analyzer module."""

import os
import io
import csv
import sys
import tempfile
import contextlib
import unittest

# Make sure we can import the module when running from tests directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import log_analyzer as la  # noqa: E402  # pylint: disable=wrong-import-position


class TestValidateIP(unittest.TestCase):
    """Tests for validate_ip utility."""

    def test_validate_ip_ipv4_ipv6_invalid(self):
        """Validate IPv4, IPv6, and reject invalid tokens."""
        self.assertTrue(la.validate_ip("192.168.1.1"))
        self.assertTrue(la.validate_ip("2001:db8::1"))
        self.assertFalse(la.validate_ip("not.an.ip"))


class TestDetectFormat(unittest.TestCase):
    """Tests for format detection helper."""

    def test_detect_format_auto(self):
        """Auto detects .csv as CSV and others as text."""
        self.assertEqual(la.detect_format("/path/to/file.csv", "auto"), "csv")
        self.assertEqual(la.detect_format("/path/to/file.log", "auto"), "text")

    def test_detect_format_override(self):
        """Honors explicit override."""
        self.assertEqual(la.detect_format("whatever.txt", "csv"), "csv")
        self.assertEqual(la.detect_format("whatever.csv", "text"), "text")


class TestCSVReaders(unittest.TestCase):
    """Tests for CSV reader behavior."""

    def test_read_ips_from_csv_happy_and_malformed(self):
        """Reads valid and invalid IPs, marking validity accordingly."""
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "sample.csv")
            with open(p, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "client_ip", "endpoint"])  # header
                writer.writerow(["t1", "1.2.3.4", "/a"])  # valid
                writer.writerow(["t2", "notanip", "/b"])  # invalid
                writer.writerow(["t3", "2001:db8::1", "/c"])  # valid IPv6

            rows = list(la.read_ips_from_csv(p, "utf-8", ip_column="client_ip"))
            self.assertEqual(rows, [("1.2.3.4", True), ("notanip", False), ("2001:db8::1", True)])

    def test_read_ips_from_csv_missing_column_raises(self):
        """Raises ValueError if configured IP column is absent."""
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "sample.csv")
            with open(p, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "ip", "endpoint"])  # no client_ip
                writer.writerow(["t1", "1.2.3.4", "/a"])  # valid

            with self.assertRaises(ValueError):
                _ = list(la.read_ips_from_csv(p, "utf-8", ip_column="client_ip"))


class TestTextReader(unittest.TestCase):
    """Tests for text reader behavior."""

    def test_read_ips_from_text(self):
        """Reads first token as IP and validates it."""
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "sample.log")
            with open(p, "w", encoding="utf-8") as f:
                f.write("8.8.8.8 GET /index\n")
                f.write("notanip GET /err\n")
                f.write("2001:db8::1 - - \"GET /\"\n")

            rows = list(la.read_ips_from_text(p, "utf-8"))
            self.assertEqual(rows, [("8.8.8.8", True), ("notanip", False), ("2001:db8::1", True)])


class TestAnalyze(unittest.TestCase):
    """Integration tests for analyze()."""

    def test_analyze_csv_counts_and_output(self):
        """CSV flow with duplicate IPs produces correct sorting and flags."""
        with tempfile.TemporaryDirectory() as td:
            # Create input CSV with duplicate IPs to exercise sorting and top-N
            in_p = os.path.join(td, "in.csv")
            out_p = os.path.join(td, "out.csv")
            with open(in_p, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["client_ip", "msg"])  # minimal header with ip column
                w.writerow(["1.1.1.1", "a"])  # 3x
                w.writerow(["2.2.2.2", "b"])  # 2x
                w.writerow(["1.1.1.1", "c"])
                w.writerow(["3.3.3.3", "d"])  # 1x
                w.writerow(["2.2.2.2", "e"])
                w.writerow(["1.1.1.1", "f"])

            buf_out = io.StringIO()
            buf_err = io.StringIO()
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                rc = la.analyze(
                    input_path=in_p,
                    output_path=out_p,
                    top_n=2,
                    encoding="utf-8",
                    delimiter=",",
                    no_header=False,
                    quiet=False,
                    ip_column="client_ip",
                    fmt_opt="auto",
                )
            self.assertEqual(rc, 0)
            # Validate stdout Top-N
            top_stdout = buf_out.getvalue()
            self.assertIn("Top 2 IPs:", top_stdout)
            self.assertIn("1. 1.1.1.1 — 3", top_stdout)
            self.assertIn("2. 2.2.2.2 — 2", top_stdout)
            # Validate CSV content, order by count desc then ip asc
            with open(out_p, "r", encoding="utf-8") as r:
                lines = [line.strip() for line in r.readlines()]
            self.assertEqual(lines[0], "ip,count,top_5")
            # Expect 1.1.1.1 first, 2.2.2.2 second, 3.3.3.3 third
            self.assertEqual(lines[1], "1.1.1.1,3,true")
            self.assertEqual(lines[2], "2.2.2.2,2,true")
            self.assertEqual(lines[3], "3.3.3.3,1,false")

    def test_analyze_text_with_malformed(self):
        """Text flow with a malformed line counts and warns, and outputs CSV."""
        with tempfile.TemporaryDirectory() as td:
            in_p = os.path.join(td, "in.log")
            out_p = os.path.join(td, "out.csv")
            with open(in_p, "w", encoding="utf-8") as f:
                f.write("9.9.9.9 something\n")
                f.write("notanip stuff\n")
                f.write("9.9.9.9 more\n")
            buf_out = io.StringIO()
            buf_err = io.StringIO()
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                rc = la.analyze(
                    input_path=in_p,
                    output_path=out_p,
                    top_n=1,
                    encoding="utf-8",
                    delimiter=",",
                    no_header=True,
                    quiet=False,
                    ip_column="client_ip",
                    fmt_opt="auto",
                )
            self.assertEqual(rc, 0)
            # stdout contains the top-1 line for 9.9.9.9
            self.assertIn("Top 1 IPs:", buf_out.getvalue())
            # stderr warns about malformed lines
            self.assertIn("malformed", buf_err.getvalue().lower())
            # CSV contains two rows (no header)
            with open(out_p, "r", encoding="utf-8") as r:
                rows = [line.strip() for line in r.readlines()]
            # Only one unique valid IP 9.9.9.9 with count 2
            self.assertEqual(rows, ["9.9.9.9,2,true"])

    def test_missing_input_returns_code_2(self):
        """Missing input path returns exit code 2 as specified."""
        with tempfile.TemporaryDirectory() as td:
            in_p = os.path.join(td, "does_not_exist.csv")
            out_p = os.path.join(td, "out.csv")
            rc = la.analyze(
                input_path=in_p,
                output_path=out_p,
                top_n=5,
                encoding="utf-8",
                delimiter=",",
                no_header=False,
                quiet=True,
                ip_column="client_ip",
                fmt_opt="auto",
            )
            self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
