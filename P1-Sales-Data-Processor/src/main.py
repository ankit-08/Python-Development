import os
import shutil
import argparse
import logging
from src.processor import SalesProcessor

ERROR_THRESHOLD = 5

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def setup_logging():
    log_dir = "logs"
    ensure_dir(log_dir)
    log_path = os.path.join(log_dir, "system.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    logging.info("🚀 Starting Sales Data Processor")
    return log_path

def main():
    parser = argparse.ArgumentParser(description="Sales Data Processor")
    parser.add_argument("input_dir", nargs="?", default=os.path.join("data", "in"))
    parser.add_argument("--out", default="reports")
    parser.add_argument("--processed", default=os.path.join("data", "out"))
    parser.add_argument("--error", default=os.path.join("data", "err"))
    args = parser.parse_args()

    log_path = setup_logging()

    for p in [args.input_dir, args.out, args.processed, args.error]:
        ensure_dir(p)

    proc = SalesProcessor()

    csv_files = [
        os.path.join(args.input_dir, f)
        for f in os.listdir(args.input_dir)
        if f.lower().endswith(".csv")
    ]

    if not csv_files:
        logging.warning("No CSV files found.")
        return

    logging.info("Processing %d file(s)...", len(csv_files))

    for csv_path in csv_files:
        fname = os.path.basename(csv_path)
        try:
            errors = proc.process_file(csv_path)

            if errors > ERROR_THRESHOLD:
                err_path = os.path.join(args.error, fname)
                shutil.move(csv_path, err_path)
                logging.warning(
                    "🚨 File %s moved to ERR (row_errors=%d > %d)",
                    fname, errors, ERROR_THRESHOLD
                )
            else:
                out_path = os.path.join(args.processed, fname)
                shutil.move(csv_path, out_path)
                logging.info(
                    "✅ File %s processed successfully (row_errors=%d)",
                    fname, errors
                )

        except Exception:
            logging.exception("❌ Fatal error processing %s", fname)
            try:
                shutil.move(csv_path, os.path.join(args.error, fname))
            except Exception as e:
                logging.error("Failed moving %s: %s", fname, e)

    proc.write_reports(args.out)
    logging.info("🧾 Reports written to %s", args.out)
    logging.info("📄 Logs saved to %s", log_path)
    logging.info("✅ All done!")

if __name__ == "__main__":
    main()
