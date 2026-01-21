from src.processor import SalesProcessor

def write_csv(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("date,product,qty,price\n")
        for r in rows:
            f.write(",".join(r) + "\n")

def test_file_with_5_or_less_errors(tmp_path):
    csv_file = tmp_path / "ok.csv"

    rows = [
        ["2025-01-01", "A", "1", "10.0"],
        ["BAD_DATE", "B", "1", "10.0"],   # error
        ["2025-01-01", "C", "x", "10.0"], # error
        ["2025-01-01", "D", "2", "20.0"],
        ["2025-01-01", "E", "3", "30.0"],
    ]

    write_csv(csv_file, rows)

    proc = SalesProcessor()
    errors = proc.process_file(csv_file)

    assert errors <= 5
    assert proc.rows_processed == 3
    assert proc.rows_skipped == 2

def test_file_with_more_than_5_errors(tmp_path):
    csv_file = tmp_path / "bad.csv"

    rows = [
        ["BAD", "A", "1", "10.0"],
        ["BAD", "B", "1", "10.0"],
        ["BAD", "C", "1", "10.0"],
        ["BAD", "D", "1", "10.0"],
        ["BAD", "E", "1", "10.0"],
        ["BAD", "F", "1", "10.0"],  # 6 errors
    ]

    write_csv(csv_file, rows)

    proc = SalesProcessor()
    errors = proc.process_file(csv_file)

    assert errors > 5
    assert proc.rows_processed == 0
    assert proc.rows_skipped == 6
