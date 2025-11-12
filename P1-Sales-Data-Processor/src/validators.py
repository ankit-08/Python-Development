# src/validators.py
from datetime import datetime

class RowValidationError(ValueError):
    """Raised when a CSV row is invalid."""

def parse_row(fields):
    """
    Parse and validate a row list -> (date_str, product, qty_int, price_float).
    fields: list-like (usually csv.reader row)
    Raises RowValidationError on invalid input.
    """
    if len(fields) < 4:
        raise RowValidationError("Too few columns")

    date_s = fields[0].strip()
    product = fields[1].strip()
    qty_s = fields[2].strip()
    price_s = fields[3].strip()

    # Validate date (YYYY-MM-DD)
    try:
        datetime.strptime(date_s, "%Y-%m-%d")
    except Exception:
        raise RowValidationError(f"Invalid date: {date_s!r}")

    if not product:
        raise RowValidationError("Empty product name")

    try:
        qty = int(qty_s)
    except Exception:
        raise RowValidationError(f"Invalid quantity: {qty_s!r}")

    try:
        price = float(price_s)
    except Exception:
        raise RowValidationError(f"Invalid price: {price_s!r}")

    return date_s, product, qty, price
