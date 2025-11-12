# src/main.py
import argparse
import logging
import os
from .processor import SalesProcessor
from .io_utils import list_csv_files

LOGFILE = "logs/errors.log"

def setup_logging(verbose=False):
    os.makedirs("logs", exist_ok=True)
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        filename=LOGFILE,
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    # Also show INFO+ to console for user visibility
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    fmt = logging.Formatter("%(levelname)s: %(message)s")
    console.setFormatter(fmt)
    logging.getLogger().addHandler(console)

def parse_args():
    p = argparse.ArgumentParser(description="Sales Data Processor")
    p.add_argument("input", help="CSV file or directory containing CSV files")
    p.add_argument("--out", "-o", default="reports", help="Output reports directory")
    p.add_argument("--verbose", action="store_true", help="Verbose logging to file")
    return p.parse_args()

def main():
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    files = list_csv_files(args.input)
    if not files:
        logger.error("No CSV files found at %s", args.input)
        return 1

    proc = SalesProcessor()
    logger.info("Processing %d file(s)...", len(files))
    proc.process_files(files)

    os.makedirs(args.out, exist_ok=True)
    proc.write_reports(args.out)

    logger.info("Done. Reports written to %s", args.out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
