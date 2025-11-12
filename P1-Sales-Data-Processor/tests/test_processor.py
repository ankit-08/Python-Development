# tests/test_processor.py
import tempfile
import os
from src.processor import SalesProcessor
from src.io_utils import write_csv

def test_basic_aggregation(tmp_path):
    # prepare a temporary csv
    csv_path = tmp_path / "sample.csv"
    header = ["Date", "Product", "Quantity", "Price"]
    rows = [
        ("2025-11-01", "ProdX", "2", "10"),
        ("2025-11-01", "ProdY", "1", "5"),
        ("2025-11-02", "ProdX", "3", "10"),
    ]
    write_csv(str(csv_path), header, rows)

    proc = SalesProcessor()
    proc.process_file(str(csv_path))

    assert proc.total_revenue == 2*10 + 1*5 + 3*10
    assert proc.product_totals["ProdX"]["quantity"] == 5
    assert proc.daily_totals["2025-11-01"]["revenue"] == 2*10 + 1*5
