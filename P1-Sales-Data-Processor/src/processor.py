# src/processor.py
import logging
from collections import defaultdict
from .validators import parse_row, RowValidationError
from .io_utils import read_csv_rows, write_text, write_csv

logger = logging.getLogger(__name__)

class SalesProcessor:
    def __init__(self):
        # product -> {'quantity': int, 'revenue': float}
        self.product_totals = defaultdict(lambda: {"quantity": 0, "revenue": 0.0})
        # date -> {'quantity': int, 'revenue': float}
        self.daily_totals = defaultdict(lambda: {"quantity": 0, "revenue": 0.0})
        self.total_revenue = 0.0
        self.rows_processed = 0
        self.rows_skipped = 0

    def process_row(self, date_str, product, qty, price):
        revenue = qty * price
        p = self.product_totals[product]
        p["quantity"] += qty
        p["revenue"] += revenue

        d = self.daily_totals[date_str]
        d["quantity"] += qty
        d["revenue"] += revenue

        self.total_revenue += revenue
        self.rows_processed += 1

    def process_file(self, filepath):
        """
        Process a single CSV file. Collects errors via logging and increments rows_skipped.
        """
        try:
            for lineno, row in enumerate(read_csv_rows(filepath, skip_header=True), start=2):
                try:
                    date_s, product, qty, price = parse_row(row)
                except RowValidationError as e:
                    logger.error("%s:%d - %s", filepath, lineno, e)
                    self.rows_skipped += 1
                    continue
                except Exception as e:
                    logger.exception("Unexpected error parsing %s:%d", filepath, lineno)
                    self.rows_skipped += 1
                    continue

                self.process_row(date_s, product, qty, price)
        except FileNotFoundError:
            logger.error("File not found: %s", filepath)
        except PermissionError:
            logger.error("Permission denied reading: %s", filepath)

    def process_files(self, filepaths):
        for f in filepaths:
            self.process_file(f)

    def generate_text_report(self):
        lines = []
        lines.append(f"Rows processed: {self.rows_processed}")
        lines.append(f"Rows skipped: {self.rows_skipped}")
        lines.append(f"Total Revenue: {self.total_revenue:.2f}")
        lines.append("")
        lines.append("Product-wise totals:")
        for prod, vals in sorted(self.product_totals.items(), key=lambda kv: -kv[1]["revenue"]):
            lines.append(f"{prod}: Qty={vals['quantity']}, Revenue={vals['revenue']:.2f}")
        lines.append("")
        lines.append("Daily totals:")
        for date, vals in sorted(self.daily_totals.items()):
            lines.append(f"{date}: Qty={vals['quantity']}, Revenue={vals['revenue']:.2f}")
        return "\n".join(lines)

    def write_reports(self, outdir):
        txt = self.generate_text_report()
        write_text(f"{outdir}/sales_summary.txt", txt)

        # product CSV
        prod_rows = [(p, v["quantity"], f"{v['revenue']:.2f}") for p, v in self.product_totals.items()]
        prod_rows.sort(key=lambda r: float(r[2]), reverse=True)
        write_csv(f"{outdir}/product_totals.csv", ["Product", "Quantity", "Revenue"], prod_rows)

        # daily CSV
        daily_rows = [(d, v["quantity"], f"{v['revenue']:.2f}") for d, v in self.daily_totals.items()]
        daily_rows.sort()
        write_csv(f"{outdir}/daily_totals.csv", ["Date", "Quantity", "Revenue"], daily_rows)
