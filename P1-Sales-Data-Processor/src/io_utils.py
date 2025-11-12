# src/io_utils.py
import os
import csv

def list_csv_files(path):
    """
    Return a list of csv file paths from 'path'.
    If path is a file, returns [path] (if .csv). If dir, returns all .csv files (non-recursive).
    """
    if os.path.isfile(path):
        return [path] if path.lower().endswith(".csv") else []
    if os.path.isdir(path):
        entries = []
        for fname in os.listdir(path):
            full = os.path.join(path, fname)
            if os.path.isfile(full) and fname.lower().endswith(".csv"):
                entries.append(full)
        return sorted(entries)
    return []

def read_csv_rows(filepath, skip_header=True):
    """
    Generator that yields rows (lists) from a CSV file.
    skip_header: if True, skips the first row.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        if skip_header:
            _ = next(reader, None)
        for row in reader:
            # Skip fully-blank rows
            if not any(cell.strip() for cell in row):
                continue
            yield row

def write_text(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        writer.writerows(rows)
