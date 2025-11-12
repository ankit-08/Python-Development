import os
import shutil
import argparse
import logging
from src.processor import SalesProcessor

def ensure_dir(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def setup_logging():
    """Configure logging to file + console."""
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
    parser = argparse.ArgumentParser(
        description=(
            "Sales Data Processor — reads from data/in, writes reports to /reports, "
            "moves processed files to /data/out, failed ones to /data/err, and logs to /logs/system.log"
        )
    )

    # --- Default directories ---
    default_input = os.path.join("data", "in")
    default_out = "reports"
    default_processed = os.path.join("data", "out")
    default_error = os.path.join("data", "err")

    parser.add_argument(
        "input_dir",
        nargs="?",
        default=default_input,
        help=f"Directory containing input CSV files (default: {default_input})"
    )
    parser.add_argument("--out", default=default_out, help=f"Reports folder (default: {default_out})")
    parser.add_argument("--processed", default=default_processed, help=f"Processed files folder (default: {default_processed})")
    parser.add_argument("--error", default=default_error, help=f"Error files folder (default: {default_error})")

    args = parser.parse_args()

    # --- Setup logging ---
    log_path = setup_logging()

    # --- Ensure directories exist ---
    for path in [args.input_dir, args.out, args.processed, args.error]:
        ensure_dir(path)

    proc = SalesProcessor()

    # --- Collect input CSVs ---
    csv_files = [
        os.path.join(args.input_dir, f)
        for f in os.listdir(args.input_dir)
        if f.endswith(".csv")
    ]

    if not csv_files:
        logging.warning(f"No CSV files found in {args.input_dir}. Nothing to process.")
        return

    logging.info(f"INFO: Processing {len(csv_files)} file(s) from {args.input_dir}/ ...")

    for csv_path in csv_files:
        try:
            proc.process_file(csv_path)
            logging.info(f"✅ Processed: {os.path.basename(csv_path)}")

            dest_path = os.path.join(args.processed, os.path.basename(csv_path))
            shutil.move(csv_path, dest_path)
            logging.info(f"📦 Moved to: {dest_path}")

        except Exception as e:
            logging.error(f"❌ Error processing {csv_path}: {e}")
            err_path = os.path.join(args.error, os.path.basename(csv_path))
            try:
                shutil.move(csv_path, err_path)
                logging.error(f"🚨 Moved to error folder: {err_path}")
            except Exception as move_err:
                logging.error(f"⚠️ Failed to move {csv_path} to error dir: {move_err}")

    proc.write_reports(args.out)
    logging.info(f"🧾 Reports written to: {args.out}")
    logging.info(f"📂 Success files moved to: {args.processed}")
    logging.info(f"🚨 Error files moved to: {args.error}")
    logging.info("✅ All done!")
    logging.info(f"📄 Logs saved to: {log_path}")

if __name__ == "__main__":
    main()
